import datetime as dt
import pytz


class Datetime():
    TZ = pytz.timezone('Asia/Ho_Chi_Minh')

    @staticmethod
    def timezone():
        return 'Asia/Ho_Chi_Minh'

    @classmethod
    def now(cls):
        current = dt.datetime.now()
        return cls.TZ.localize(current)

    @staticmethod
    def utcnow():
        return dt.datetime.utcnow
    
    @staticmethod
    def is_datetime(object):
        return isinstance(object, dt.datetime)
