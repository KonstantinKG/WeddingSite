import os
import sys
import logging
import datetime
import re
from logging.handlers import TimedRotatingFileHandler

dirname = os.path.dirname(__file__)
dirname = os.path.join(dirname, '../logs')

if not os.path.exists(dirname):
    os.mkdir(dirname)

date = datetime.date.today().strftime('%Y%m%d')


class Logger:
    def __init__(self):
        self.FORMATTER = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
        self.LOG_FILE = os.path.join(dirname, 'my_app.' + date + '.log')

    @staticmethod
    def namer(name):
        a = name[-28:][-8:]
        date1 = datetime.datetime.strptime(a, '%Y%m%d')
        date1 = date1 + datetime.timedelta(days=1)
        str_date = datetime.datetime.strftime(date1, '%Y%m%d')
        name = name.replace('.' + date + '.log', '') + '.log'
        return name.replace(a, str_date)

    def get_file_handler(self):
        file_handler = TimedRotatingFileHandler(self.LOG_FILE, when='midnight', backupCount=10, encoding='utf-8')
        file_handler.suffix = '%Y%m%d'
        file_handler.namer = self.namer
        file_handler.extMatch = re.compile(r"^\d{8}$")
        file_handler.setFormatter(self.FORMATTER)
        return file_handler

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.FORMATTER)
        return console_handler

    def get_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        logger.propagate = False
        return logger
