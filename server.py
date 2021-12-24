from flask import Flask, jsonify, request, json, current_app
from flask_pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from conf import *
import configparser
from routes import user, error
from routes.file_queue import *
from threading import Thread
from log.log import *
import sys
import pymysql
import time
from datetime import datetime

# use flask
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# call config
conf = configparser.ConfigParser()
conf.read('./conf/config.ini')

mysql_db = pymysql.connect(
    host=conf['MYSQL_SETTINGS']['host'], 
    user=conf['MYSQL_SETTINGS']['user'], 
    db=conf['MYSQL_SETTINGS']['database'], 
    password=conf['MYSQL_SETTINGS']['password'], 
    charset=conf['MYSQL_SETTINGS']['charset']
    )

# mongodb setting
mongo_uri = conf['MONGODB_SETTINGS']['MONGO_URI']
mongo_db = conf['MONGODB_SETTINGS']['MONGO_DBNAME']
client = MongoClient(mongo_uri)

# call log
log = Log("__name__")

with app.app_context():
    # connect_timeout=5000
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
        client.server_info()
        mg_db = client[mongo_db]
    except ConnectionFailure or ServerSelectionTimeoutError as e:
        log.error_msg(e)
        
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)

# run flask
if __name__ == "__main__":
    log.console()
    log.debug()
    log.access()
    log.error()
    # mg_db = connection()

    thread = Thread(target=fn_queue, args=(queue, ), daemon=True)
    thread.start()

    # registering contents in Blueprint
    app.register_blueprint(user.bp)
    app.register_blueprint(error.error)

    app.run(host=conf['SERVER']['host'],
            debug=True, port=conf['SERVER']['port'])
