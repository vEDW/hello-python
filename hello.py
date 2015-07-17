import os
import uuid
import urlparse
import redis
import json
import urllib
import requests

from flask import Flask
from flask import request
from flask import jsonify


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
	r_server.incr('counter')
	if request.headers.getlist("X-Forwarded-For"):
   		ipaddress = request.headers.getlist("X-Forwarded-For")[0]
		print "X-Forwarded-For : " + ipaddress
		print type(ipaddress)
#		newip = %s (ipaddress)
#		print type(newip)
#		print "newip : " + newip

	else:
   		ipaddress = request.remote_addr

#	response = urllib.request.urlopen('http://freegeoip.net/json/'+ipaddress[0]).read().decode('utf-8')
	responseJson = requests.get('http://freegeoip.net/json/'+'213.49.119.86').json()
	country = responseJson.get("country_code")
#	country="test"

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

	</body>
	</html>
	""".format(COLOR,my_uuid,r_server.get('counter'),ipaddress,country)




if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
