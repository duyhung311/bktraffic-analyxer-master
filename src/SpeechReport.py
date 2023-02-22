import time
import io
import soundfile
import ffmpeg
from src.utils.PPrinter import PPrinter
from src.utils.database import ProcessStatus, SpeechReport, Street, Segment, SegmentReport
from src.utils.Datetime import Datetime
from src.asr.interface import ASR
from src.slot_filling.interface import SlotFilling
from src.slot_filling.utils import sf2json


Printer = PPrinter()
converter = (
    ffmpeg
    .input('pipe:')
    .output('pipe:', format='wav', acodec='pcm_s16le', ar='16k')
    .overwrite_output()
)


def find_segment_center_point(segment_document):
    start, end = segment_document.polyline['coordinates']
    return [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]


def map_segment_to_center_point(segment_document):
    center_point = find_segment_center_point(segment_document)
    res = {
        'segment': segment_document.id,
        'center_point': {
            'coordinates': center_point,
            'type': 'Point'
        }
    }
    return res

def inference_speech_report(speech_report):
    speech2text = ASR()
    slot_filling = SlotFilling()

    record = speech_report.speech_record
    input = record.dataEnhanced or record.data

    if not input:
        Printer.error(f"[Speech Report] Audio not found in speech record {record.id}")
        raise Exception('[Speech Report] Audio not found')

    out, _ = converter.run(capture_stdout=True, input=input, quiet=True)
    speech, _ = soundfile.read(io.BytesIO(out))

    # ASR
    nbests = speech2text.to_text(speech)
    text, *_ = nbests[0]
    clean_text = speech2text.text_normalizer(text)
    Printer.log(f"ASR hypothesis: {clean_text}")
    Printer.log('*' * 50)

    # Slot filling
    sf = slot_filling.predict(clean_text.lower())
    result = sf2json(sf, clean_text.lower())
    Printer.log('[Speech Report] Intermediate parsed result', result)
    street_name = result.pop('street', None)

    if speech_report.segments:
        result['segments'] = Segment.objects(id__in=speech_report.segments)
    else:
        street_ids = Street.objects(name__icontains=street_name).only('id').distinct('id')
        result['segments']
    
    selected_fields = ['segments', 'velocity', 'causes', 'description']
    return { k : v for k, v in result.items() if k in selected_fields }

def process_speech_report(speech_report_id, force=False):
    Printer.log('[Speech Report] Process report:', speech_report_id)
    start = time.time()
    processed_date = Datetime.now()
    speech_report = SpeechReport.objects.get(id=speech_report_id)
    if not speech_report:
        return Printer.error(f"[Speech Report] Report {speech_report_id} not found")
    if speech_report.processed_date and not force:
        return Printer.warn(f"[Speech Report] Report {speech_report_id} was processed")
    
    response = inference_speech_report(speech_report)
    segments = response.pop('segments', [])

    data = {
        'source': speech_report.source,
        'user': speech_report.user,
        'period_id': speech_report.period_id,
        'createdAt': speech_report.createdAt,
    }
    data['updatedAt'] = processed_date
    data = {**data, **response}

    segment_coords = map(map_segment_to_center_point, segments)
    segment_reports = map(lambda coord: {**coord, **data}, segment_coords)
    segment_reports = filter(lambda report: 'segment' in report, segment_reports)

    try:
        segment_reports = [SegmentReport.from_dict(report) for report in segment_reports]
        [report.validate() for report in segment_reports]

        SpeechReport.objects(id=speech_report_id).update_one(
            set__processed_date=processed_date,
            set__processed_status=ProcessStatus.SUCCESS
        )
        Printer.success(f"[Speech Report] process: {time.time() - start}s")
        return segment_reports
    except Exception as e:
        SpeechReport.objects(id=speech_report_id).update_one(
            set__processed_date=processed_date,
            set__processed_status=ProcessStatus.FAIL
        )
        raise e

def process_speech_reports_job():
    start = time.time()

    speech_reports = SpeechReport.objects(__raw__={ 'processed_date': None })
    Printer.log(f"Found {speech_reports.count()} new speech report(s)")
    processed_date = Datetime.now()
    for speech_report in speech_reports:
        single_start = time.time()

        # Preprocessing
        response = inference_speech_report(speech_report)
        segments = response.pop('segments', [])

        # Pick necessary attributes
        data = {
            'source': speech_report.source,
            'user': speech_report.user,
            'period_id': speech_report.period_id,
            'createdAt': speech_report.createdAt,
        }
        data['updatedAt'] = processed_date
        data = {**data, **response}

        segment_coords = map(map_segment_to_center_point, segments)
        segment_reports = map(lambda coord: {**coord, **data}, segment_coords)
        segment_reports = filter(lambda report: 'segment' in report, segment_reports)

        try:
            segment_reports = [SegmentReport.from_dict(report) for report in segment_reports]
            [report.validate() for report in segment_reports]

            SegmentReport.objects.insert(segment_reports)
            SpeechReport.objects(id=speech_report.id).update_one(
                set__processed_date=processed_date,
                set__processed_status=ProcessStatus.SUCCESS
            )
            Printer.log(f"[Speech Report] Process report {speech_report.id}: {time.time() - single_start}s")
        except:
            SpeechReport.objects(id=speech_report.id).update_one(
                set__processed_date=processed_date,
                set__processed_status=ProcessStatus.FAIL
            )
            Printer.warn(f"[Speech Report] Fail to process speech report {speech_report.id}")

    Printer.success(f"[Speech Report] Batch process: {time.time() - start}s")
