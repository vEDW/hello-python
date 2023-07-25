import os
import uuid
import json
import requests
import time
import sys, errno

from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)
my_uuid = str(uuid.uuid1())

MESSAGE = os.getenv('MESSAGE')
MY_NODE_NAME = os.getenv('MY_NODE_NAME')

print("Message : " + str(MESSAGE))

def shutdown_server():
	sys.exit(errno.EINTR)

@app.route('/')
def hello():
	hostname = os.uname()[1]
	returntext = hostname + " - " + str(MESSAGE) + " - " + str(MY_NODE_NAME)
	print(request.remote_addr)
	return returntext

@app.route('/whoami')
def whoami():
	returntext = "<br/>" + "REMOTE_ADDR=" + str(request.environ.get('REMOTE_ADDR')) + "\r\n"
	returntext = returntext + "<br/>" + "HTTP_X_FORWARDED_FOR=" + str(request.environ.get('HTTP_X_FORWARDED_FOR')) + "\r\n"
	returntext = returntext + "<br/>" + "X-Real-IP=" + str(request.environ.get('X-Real-IP')) + "\r\n"
	print(returntext)
	return returntext


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.errorhandler(404)
def not_found(error):
	return "404 - You're doomed !", 404


@app.errorhandler(500)
def not_found(error):
	return "500 - I failed !  :/ ", 500

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
