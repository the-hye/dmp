# log.py
import logging
import logging.handlers
from flask import request, json

print("========= start log.py =========")

class Log():
    # initialize log information
    def __init__(self,name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s \t %(levelname)s \t %(message)s')

    # get all logs on console   
    def console(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(stream_handler)
        return self.logger

    # get all logs on debug file
    def debug(self):
        file_handler = logging.handlers.TimedRotatingFileHandler(filename
         = "log/debug.log", when = 'midnight', interval=1, backupCount=5, encoding='utf-8')
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)
        return self.logger

    # get user access logs on access file
    def access(self):
        logger_http =  logging.getLogger('werkzeug')
        accesshandler = logging.FileHandler(filename='log/access.log')
        logger_http.addHandler(accesshandler)
        return self.logger  

    # get user error logs on error file 
    def error(self):
        error_handler=logging.FileHandler(filename='log/error.log')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(self.formatter)
        self.logger.addHandler(error_handler)
        return self.logger

    def error_msg(self, err):
        error_msg_handler=logging.FileHandler(filename='log/error.log')
        error_msg_handler.setLevel(logging.ERROR)
        error_msg_handler.setFormatter(self.formatter)
        self.logger.addHandler(error_msg_handler)
        self.logger.removeHandler(error_msg_handler)
        return self.logger.error(err)

    # get user logs
    def get_log(self, level):
        ip = request.environ.get('HTTP_X_REAL_IP',request.remote_addr)
        url = request.url
        header = json.dumps(dict(request.headers))
        body = request.get_json()
        message = "{}\tip : {}\turl : {}\theader : {}\tbody : {}\t".format(
        request.method, ip, url, header, str(body))

        #print user logs by each level
        if level == 'debug':
            return self.logger.debug(message)
        elif level == 'info':
            return self.logger.info(message)
        else:
            return self.logger.error(message)

    