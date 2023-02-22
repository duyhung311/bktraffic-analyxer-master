import os
import io
import ffmpeg
import soundfile
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import udf
from src.asr.interface import ASR
from src.slot_filling.interface import SlotFilling
from src.slot_filling.utils import sf2json


converter = (
    ffmpeg
    .input('pipe:')
    .output('pipe:', format='wav', acodec='pcm_s16le', ar='16k')
    .overwrite_output()
)

SPEECH_RECORDS = 'SpeechRecords'


def find_segment_center_point(segment_document):
    start, end = segment_document['polyline']['coordinates']
    return [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]


def map_segment_to_center_point(segment_document):
    center_point = find_segment_center_point(segment_document)
    res = {
        'segment': segment_document['_id'],
        'center_point': {
            'coordinates': center_point,
            'type': 'Point'
        }
    }
    return res

def inference(speech_record):
    speech2text = ASR()
    slot_filling = SlotFilling()

    # Preprocessing
    out, _ = converter.run(capture_stdout=True,
                           input=speech_record, quiet=True)
    speech, _ = soundfile.read(io.BytesIO(out))

    # ASR
    nbests = speech2text.to_text(speech)
    text, *_ = nbests[0]
    clean_text = speech2text.text_normalizer(text)

    # Slot filling
    sf = slot_filling.predict(clean_text.lower())
    response = sf2json(sf, clean_text.lower())

    return response


def main():
    db_uri = os.getenv('DATABASE_URI')

    spark = (SparkSession.builder
                         .appName('Speech Report Inference')
                         .config('spark.mongodb.input.uri', db_uri)
                         .config('spark.mongodb.input.readPreference.name', 'primaryPreferred')
                         .config('spark.mongodb.output.uri', db_uri)
                         .getOrCreate())
    logger = spark._jvm.org.apache.log4j
    logger.LogManager.getRootLogger().setLevel(logger.Level.FATAL)

    pipeline = "{ '$match': { 'script': { '$exists': true } } }"
    df = (spark.read
               .format('mongo')
               .option('collection', SPEECH_RECORDS)
               .option('pipeline', pipeline)
               .load())

    inference_udf = udf(inference, StringType()).asNondeterministic()
    df.select(inference_udf(df['data']).alias('inference')).show()


if __name__ == '__main__':
    main()
