import os
import uuid
import urlparse
import redis
import json

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r_server = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])

from flask import Flask
app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"

COLOR = BLUE

r_server.set('counter',0)

@app.route('/')
def hello():
	global r_server
	r_server.incr('counter')
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



	</body>
	</html>
	""".format(COLOR,my_uuid,r_server.get('counter'))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
