import os
import uuid
import redis
import json
import requests

from flask import Flask
from flask import request
from flask import jsonify

# Loggly logging
import logging
import logging.config
import loggly.handlers

logging.config.fileConfig('python.conf')
logger = logging.getLogger('myLogger')

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r_server = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])


app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"

COLOR = BLUE

@app.route('/admin')

def otherfct():
	print "admin"


@app.route('/')

def hello():
	global r_server
	global logger
	logger.info('Begin hello()')
	r_server.incr('counter')
	if request.headers.getlist("X-Forwarded-For"):
   		logger.info("Getting X-Forwarded")
		ipaddress = request.headers.getlist("X-Forwarded-For")[0]
		print "X-Forwarded-For : " + ipaddress
		logger.info(ipaddress)
		print type(ipaddress)
		idx=str(ipaddress).index(',')
		address = ipaddress[0:idx]
		print address
	else:
   		logger.info("Getting remote_addr")
   		ipaddress = request.remote_addr
   		logger.info(ipaddress)

	logger.info('Get freegeoip for : '  + address)
	print "requesting freegeoip"
	responseJson = requests.get('http://freegeoip.net/json/' + address).json()
	print responseJson
	logger.info(responseJson)
	country = responseJson.get("country_name")
	r_server.incr(country)

	return """

	<html>
	<body bgcolor="{}">

	<center><h1><font color="white">Welcome to Redis App !<br/>
	</center>

	<center><h1><font color="white">I'm GUID:<br/>
	{}
	</center>

	<center><h1><font color="white">Hits count:<br/>
	{}
	</center>

	<center><h1><font color="white">Your IP :<br/>
	{}
	</center>

	<center><h1><font color="white">Your Country :<br/>
	{}
	</center>

	<center><h1><font color="white">Hits for your Country :<br/>
	{}
	</center>


	</body>
	</html>
	""".format(COLOR,my_uuid,r_server.get('counter'),address,country,r_server.get(country))

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
