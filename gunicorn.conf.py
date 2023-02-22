import os
import app
from src.utils.PPrinter import PPrinter
from src.utils.Datetime import Datetime


wsgi_app = 'app:main()'
bind = f"0.0.0.0:{os.getenv('FLASK_RUN_PORT')}"
workers = 2
threads = 2
loglevel = 'info'
name = 'bktraffic-analyxer'
worker_class = 'gthread'
accesslog = PPrinter.log_path()
access_log_format = f"[{Datetime.now()}] | %(h)s %(l)s %(u)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s'"


def on_starting(server):
    app.init()

def on_exit(server):
    app.exit()
