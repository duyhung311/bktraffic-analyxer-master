import os
import logging
from .Datetime import Datetime

logger = logging.getLogger(__name__)
LOG_DIR = 'logs'

class PPrinter():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def __init__(self, log=True):
        self.enable_log = log

        if log and not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

    def __to_string(self, list_str):
        return ' '.join(str(s) if type(s) != str else s for s in list_str)

    def __log(self, text):
        if not self.enable_log:
            return

        current_timestamp = Datetime.now()
        log_path = PPrinter.log_path()
        with open(log_path, 'a+') as f:
            f.write(f"[{current_timestamp}] | {text}\n")
    
    def __send(self, wrapper, *argv):
        text = self.__to_string(argv)
        self.__log(text)
        print(f"{wrapper}{text}{self.ENDC}")
        return text

    def success(self, *argv):
        self.__send(self.OKGREEN, *argv)

    def log(self, *argv):
        text = self.__send(self.OKBLUE, *argv)
        logger.info(text)

    def warn(self, *argv):
        text = self.__send(self.WARNING, *argv)
        logger.warning(text)
    
    def error(self, *argv):
        text = self.__send(self.FAIL, *argv)
        logger.error(text)
    
    @staticmethod
    def log_path():
        current_timestamp = Datetime.now()
        log_file = f"{current_timestamp.strftime('%Y%m%d')}.log"
        return os.path.join(LOG_DIR, log_file)

def to_string(*argv):
    return ' '.join(str(arg) if type(arg) != str else arg for arg in argv)

if __name__ == '__main__':
    Printer = PPrinter()
    Printer.success('[PPrinter Test] success', 1)
    Printer.log('[PPrinter Test] log', 2)
    Printer.warn('[PPrinter Test] warn', True, 3)
    Printer.error('[PPrinter Test] error', False, 0)
