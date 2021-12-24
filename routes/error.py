from flask import Blueprint
from server import *
from log.log import *

# call Blueprint
error = Blueprint("error", __name__)

# call log
# logger_error = logging.getLogger("__name__")
log = Log("__name__") # http error 안찍힘

# get_error_log
def get_error_log(err):
    ip = request.environ.get('HTTP_X_REAL_IP',request.remote_addr)
    return log.error_msg("{}\tip : {}\turl : {}\t{}".format(request.method, ip, request.url, err))
    
# manage 404 error
@error.app_errorhandler(404)
def err_404(err):
    get_error_log(err)
    return err

# manage 405 error
@error.app_errorhandler(405)
def err_405(err):
    get_error_log(err)
    return jsonify({"message" : "ERROR 405!"}), 405

# manage exception error
@error.app_errorhandler(Exception)
def err_except(err):
    get_error_log(err)
    print('error exception')
    return jsonify({"message" : "ERROR!!"})