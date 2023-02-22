import os
import subprocess
import json
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from bson.objectid import ObjectId
from src import velocity_estimator
from src.velocity_estimator.interface import VelocityEstimator
from src.utils.response import CustomResponse
from src.utils.serializer import SegmentReportSerializer
from src.utils.validator import InferenceValidator, SeqInferenceValidator, validate_input
from src.utils.PPrinter import PPrinter
import src.utils.database as Database
from src.utils.Datetime import Datetime
from src.utils.download_and_unzip import download_and_unzip
from src.SpeechReport import process_speech_report, process_speech_reports_job


app = Flask(__name__)
cors = CORS(app, resources={'*': {'origins': '*'}})
api = Api(app)
Printer = PPrinter()


def page_not_found(e):
  return CustomResponse(status=404)
app.register_error_handler(404, page_not_found)

@app.route('/_health', methods=['GET'])
def health():
    return 'OK'

@app.route('/inference', methods=['POST'])
def normal_inference():
    """
    Input:
    - Dict(
        segment_id (List[int]): a list of segment ID
        timestamp (int | float | List[int] | List[float]): timestamp in seconds
    )
    Output:
    - Dict(segment_id: List, velocity: List, LOS: List)
    """
    req = request.json # dictionary
    errors, data = validate_input(req, InferenceValidator)

    if len(errors) != 0:
        [Printer.error(e['message']) for e in errors]
        return CustomResponse(status=400, errors=errors)
    
    global velocity_estimator
    res = velocity_estimator.inference(data)
    try:
        return CustomResponse(status=200, data=json.dumps(res))
    except Exception as e:
        Printer.error(e)
        return CustomResponse(status=500)

@app.route('/seq_inference', methods=['POST'])
def seq_inference():
    """
    Input:
    - Dict(
        segment_id (List[int]): a list of segment ID
        timestamp (int | float): timestamp in seconds
    )
    Output:
    - Dict(segment_id: List, velocity: List, LOS: List, ETA: List)
    """
    req = request.json
    errors, data = validate_input(req, SeqInferenceValidator)

    if len(errors) != 0:
        Printer.error(e)
        return CustomResponse(status=400, errors=errors)

    try:
        global velocity_estimator
        res = velocity_estimator.sequence_inference(data)
        return CustomResponse(status=200, data=json.dumps(res))
    except Exception as e:
        Printer.error(e)
        return CustomResponse(status=500)

@app.route('/speech_report/<id>', methods=['GET'])
def speech_report(id):
    """
    Force inferencing speech report to segment report
    """
    force = request.args.get('force') == 'true' or False
    try:
        reports = process_speech_report(ObjectId(id), force)
        res = [SegmentReportSerializer.serialize(report) for report in reports] if reports else []
        return CustomResponse(status=200, data=json.dumps(res))
    except Exception as e:
        Printer.error(e)
        return CustomResponse(status=500)

@app.route('/speech_reports', methods=['GET'])
def batch_process_speech_reports():
    process_speech_reports_job()
    return CustomResponse(status=200)


def init():
    Printer.success('=' * 10, f"Start {os.getenv('FLASK_ENV')} server :", Datetime.now(), '=' * 10)
    download_and_unzip(force=False)
    Printer.success('[SERVER] Server ready')
    subprocess.call('nohup python3 cron_job.py >/dev/null 2>&1 &', shell=True)
   #>/dev/null 2>&1 &
def exit():
    Printer.success('[SERVER] Stop server :', Datetime.now())

def main():
    database_uri = os.getenv('DATABASE_URI')
    Database.init(database_uri)

    # global velocity_estimator
    # velocity_estimator = VelocityEstimator('2022-04-10', '2022-04-11')

    return app

if __name__ == '__main__':
    init()
    app = main()
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=bool(os.getenv('FLASK_DEBUG_MODE', False)))
