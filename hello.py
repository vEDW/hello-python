import os
import uuid
import redis
import json
import requests
import time
#import sendmail

from flask import Flask
from flask import request
from flask import jsonify

# Loggly logging
import logging
import logging.config
import loggly.handlers

print "start vedw"

logging.config.fileConfig('python.conf')
logger = logging.getLogger('myLogger')

print "start redis"

#IF PWS :

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r_server = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])

#IF PCF on premises/vcloud
#rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['p-redis'][0]
#credentials = rediscloud_service['credentials']
#r_server = redis.Redis(host=credentials['host'], port=credentials['port'], password=credentials['password'])


#import sendgrid

print "start sendgrid"

#sendgrid_service = json.loads(os.environ['VCAP_SERVICES'])['sendgrid'][0]
#credentials = sendgrid_service['credentials']
#sendgrid_server = sendgrid.SendGridClient(credentials['username'], credentials['password'])


#def sendmsg (content):
#    message = sendgrid.Mail()
#    message.add_to('eric <eric@vedw.eu>')
#    message.set_subject('vedwapp')
#    message.set_html(content)
#    message.set_text(content)
#    message.set_from('vedw PWS <eric@vedw.eu>')
#    status, msg = sendgrid_server.send(message)
#    print status


country_json = {"BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", "BG": "Bulgaria", "BA": "Bosnia and Herzegovina", "BB": "Barbados", "WF": "Wallis and Futuna", "BL": "Saint Barthelemy", "BM": "Bermuda", "BN": "Brunei", "BO": "Bolivia", "BH": "Bahrain", "BI": "Burundi", "BJ": "Benin", "BT": "Bhutan", "JM": "Jamaica", "BV": "Bouvet Island", "BW": "Botswana", "WS": "Samoa", "BQ": "Bonaire, Saint Eustatius and Saba ", "BR": "Brazil", "BS": "Bahamas", "JE": "Jersey", "BY": "Belarus", "BZ": "Belize", "RU": "Russia", "RW": "Rwanda", "RS": "Serbia", "TL": "East Timor", "RE": "Reunion", "TM": "Turkmenistan", "TJ": "Tajikistan", "RO": "Romania", "TK": "Tokelau", "GW": "Guinea-Bissau", "GU": "Guam", "GT": "Guatemala", "GS": "South Georgia and the South Sandwich Islands", "GR": "Greece", "GQ": "Equatorial Guinea", "GP": "Guadeloupe", "JP": "Japan", "GY": "Guyana", "GG": "Guernsey", "GF": "French Guiana", "GE": "Georgia", "GD": "Grenada", "GB": "United Kingdom", "GA": "Gabon", "SV": "El Salvador", "GN": "Guinea", "GM": "Gambia", "GL": "Greenland", "GI": "Gibraltar", "GH": "Ghana", "OM": "Oman", "TN": "Tunisia", "JO": "Jordan", "HR": "Croatia", "HT": "Haiti", "HU": "Hungary", "HK": "Hong Kong", "HN": "Honduras", "HM": "Heard Island and McDonald Islands", "VE": "Venezuela", "PR": "Puerto Rico", "PS": "Palestinian Territory", "PW": "Palau", "PT": "Portugal", "SJ": "Svalbard and Jan Mayen", "PY": "Paraguay", "IQ": "Iraq", "PA": "Panama", "PF": "French Polynesia", "PG": "Papua New Guinea", "PE": "Peru", "PK": "Pakistan", "PH": "Philippines", "PN": "Pitcairn", "PL": "Poland", "PM": "Saint Pierre and Miquelon", "ZM": "Zambia", "EH": "Western Sahara", "EE": "Estonia", "EG": "Egypt", "ZA": "South Africa", "EC": "Ecuador", "IT": "Italy", "VN": "Vietnam", "SB": "Solomon Islands", "ET": "Ethiopia", "SO": "Somalia", "ZW": "Zimbabwe", "SA": "Saudi Arabia", "ES": "Spain", "ER": "Eritrea", "ME": "Montenegro", "MD": "Moldova", "MG": "Madagascar", "MF": "Saint Martin", "MA": "Morocco", "MC": "Monaco", "UZ": "Uzbekistan", "MM": "Myanmar", "ML": "Mali", "MO": "Macao", "MN": "Mongolia", "MH": "Marshall Islands", "MK": "Macedonia", "MU": "Mauritius", "MT": "Malta", "MW": "Malawi", "MV": "Maldives", "MQ": "Martinique", "MP": "Northern Mariana Islands", "MS": "Montserrat", "MR": "Mauritania", "IM": "Isle of Man", "UG": "Uganda", "TZ": "Tanzania", "MY": "Malaysia", "MX": "Mexico", "IL": "Israel", "FR": "France", "IO": "British Indian Ocean Territory", "SH": "Saint Helena", "FI": "Finland", "FJ": "Fiji", "FK": "Falkland Islands", "FM": "Micronesia", "FO": "Faroe Islands", "NI": "Nicaragua", "NL": "Netherlands", "NO": "Norway", "NA": "Namibia", "VU": "Vanuatu", "NC": "New Caledonia", "NE": "Niger", "NF": "Norfolk Island", "NG": "Nigeria", "NZ": "New Zealand", "NP": "Nepal", "NR": "Nauru", "NU": "Niue", "CK": "Cook Islands", "XK": "Kosovo", "CI": "Ivory Coast", "CH": "Switzerland", "CO": "Colombia", "CN": "China", "CM": "Cameroon", "CL": "Chile", "CC": "Cocos Islands", "CA": "Canada", "CG": "Republic of the Congo", "CF": "Central African Republic", "CD": "Democratic Republic of the Congo", "CZ": "Czech Republic", "CY": "Cyprus", "CX": "Christmas Island", "CR": "Costa Rica", "CW": "Curacao", "CV": "Cape Verde", "CU": "Cuba", "SZ": "Swaziland", "SY": "Syria", "SX": "Sint Maarten", "KG": "Kyrgyzstan", "KE": "Kenya", "SS": "South Sudan", "SR": "Suriname", "KI": "Kiribati", "KH": "Cambodia", "KN": "Saint Kitts and Nevis", "KM": "Comoros", "ST": "Sao Tome and Principe", "SK": "Slovakia", "KR": "South Korea", "SI": "Slovenia", "KP": "North Korea", "KW": "Kuwait", "SN": "Senegal", "SM": "San Marino", "SL": "Sierra Leone", "SC": "Seychelles", "KZ": "Kazakhstan", "KY": "Cayman Islands", "SG": "Singapore", "SE": "Sweden", "SD": "Sudan", "DO": "Dominican Republic", "DM": "Dominica", "DJ": "Djibouti", "DK": "Denmark", "VG": "British Virgin Islands", "DE": "Germany", "YE": "Yemen", "DZ": "Algeria", "US": "United States", "UY": "Uruguay", "YT": "Mayotte", "UM": "United States Minor Outlying Islands", "LB": "Lebanon", "LC": "Saint Lucia", "LA": "Laos", "TV": "Tuvalu", "TW": "Taiwan", "TT": "Trinidad and Tobago", "TR": "Turkey", "LK": "Sri Lanka", "LI": "Liechtenstein", "LV": "Latvia", "TO": "Tonga", "LT": "Lithuania", "LU": "Luxembourg", "LR": "Liberia", "LS": "Lesotho", "TH": "Thailand", "TF": "French Southern Territories", "TG": "Togo", "TD": "Chad", "TC": "Turks and Caicos Islands", "LY": "Libya", "VA": "Vatican", "VC": "Saint Vincent and the Grenadines", "AE": "United Arab Emirates", "AD": "Andorra", "AG": "Antigua and Barbuda", "AF": "Afghanistan", "AI": "Anguilla", "VI": "U.S. Virgin Islands", "IS": "Iceland", "IR": "Iran", "AM": "Armenia", "AL": "Albania", "AO": "Angola", "AQ": "Antarctica", "AS": "American Samoa", "AR": "Argentina", "AU": "Australia", "AT": "Austria", "AW": "Aruba", "IN": "India", "AX": "Aland Islands", "AZ": "Azerbaijan", "IE": "Ireland", "ID": "Indonesia", "UA": "Ukraine", "QA": "Qatar", "MZ": "Mozambique","":"hidden"}


app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"

COLOR = GREEN


@app.route('/')

def hello():
	print "start hello"
	hello_starttime = time.time()
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
	print "requesting ipinfo.io"
	start_time = time.time()
	responseJson = requests.get('http://ipinfo.io/' + address + "/json").json()
	print responseJson
	exec_time = time.time() - start_time
	exec_timestr = "ipinfo.io --- %s seconds ---" % exec_time
	print exec_timestr
	logger.info(responseJson)
	logger.info(exec_timestr)

	country = responseJson.get("country")
	print country
	country = country_json.get(country)
	print country

	r_server.incr(country)
	page_time = time.time() - hello_starttime
	page_timestr = "--- %s seconds ---" % page_time

	now = time.ctime(int(time.time()))
 	print("the now time is ") + str(now)

	pagebody = str(now) + " " + address + " " + country

#	sendmsg(pagebody)

	return """

	<html>
	<body bgcolor="{}">

	<center><h1><font color="white">Welcome to the New Proximus Demo !<br/>
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


	<center><h1><font color="white">Page processing time :<br/>
	{}
	</center>


	</body>
	</html>
	""".format(COLOR,my_uuid,r_server.get('counter'),address,country,r_server.get(country),page_timestr)


@app.route('/blue')
def setblue():
	global COLOR
	COLOR = BLUE
	return "switched to BLUE"

@app.route('/green')
def setgreen():
	global COLOR
	COLOR = GREEN
	return "switched to GREEN"

@app.errorhandler(404)
def not_found(error):
	return "You're doomed !", 404


@app.errorhandler(500)
def not_found(error):
	return "I failed !  :/ ", 500

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
