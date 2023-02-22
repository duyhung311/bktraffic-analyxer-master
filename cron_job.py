import os
import requests
import time
import schedule
from src.utils.PPrinter import PPrinter


SERVER_URL = f"http://127.0.0.1:{os.getenv('FLASK_RUN_PORT')}"
Printer = PPrinter()

def batch_process_speech_reports():
    Printer.log('Run batch process speech reports')
    url = f"{SERVER_URL}/speech_reports"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            Printer.success('OK')
        else:
            Printer.error('Something went wrong!')
    except requests.exceptions.ConnectionError:
        Printer.log('Connection error. Stop cron job')
        quit()


if __name__ == '__main__':
    Printer.success('Cron job connect', SERVER_URL)
    schedule.every(5).seconds.do(batch_process_speech_reports)
    Printer.success(schedule.get_jobs())
    while True:
        schedule.run_pending()
        time.sleep(1)
