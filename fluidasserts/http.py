import requests
from requests.auth import HTTPDigestAuth
from requests_oauthlib import OAuth1
import logging 
import re

regex = {
	'access-control-allow-origin' : '^https?:\\/\\/.*$',
	'cache-control' : 'private, no-cache, no-store, max-age=0, no-transform',
	'content-security-policy' : '^([a-zA-Z]+\\-[a-zA-Z]+|sandbox).*$',
	'content-type' : '^(\\s)*.+(\\/|-).+(\\s)*;(\\s)*charset.*$',
	'expires' : '^\\s*0\\s*$',
	'pragma' : '^\\s*no-cache\\s*$',
	'strict-transport-security' : '^\\s*max\\-age=\\s*\\d+\\s.*',
	'x-content-type-options' : '^\\s*nosniff\\s*$',
	'x-frame-options' : '^\\s*(deny|allow-from|sameorigin).*$',
	'x-permitted-cross-domain-policies' : '^\\s*master\\-only\\s*$',
	'x-xss-protection' : '^1(; mode=block)?$'
}

def __get_request(url, auth = None):
	try:
		return requests.get(url, verify=False, auth = auth)
	except ConnectionError:
		logging.error('Sin acceso a %s , %s', url, 'ERROR')	

def __post_request(url, data = ""):
	try:
		return requests.post(url, verify=False, data=data)
	except ConnectionError:
		logging.error('Sin acceso a %s , %s', url, 'ERROR')	
		
def formauth_by_statuscode(url, code,**formargs):
	http_req = __post_request(url,formargs)
	if http_req.status_code == code:
		logging.info('POST Authentication %s, Details=%s, %s', url, "Success with "+str(formargs), "OPEN") 
	else:
		logging.info('POST Authentication %s, Details=%s, %s', url, "Error code ("+str(http_req.status_code)+") " + str(formargs), "CLOSE") 

def formauth_by_response(url, text,**formargs):
	http_req = __post_request(url,formargs)
	if http_req.text.find(text) >= 0:
		logging.info('POST Authentication %s, Details=%s, %s', url, "Success with "+str(formargs), "OPEN") 
	else:
		logging.info('POST Authentication %s, Details=%s, %s', url, "Error text ("+http_req.text+") " + str(formargs), "CLOSE") 
	
def basic_auth(url, user, passw):
	r = __get_request(url, (user,passw))
	if __get_request(url).status_code == 401:
		if r.status_code == 200:
			logging.info('HTTPBasicAuth %s, Details=%s, %s', url, "Success with [ "+user+" : "+passw+" ]", "OPEN")
		else:
			logging.info('HTTPBasicAuth %s, Details=%s, %s', url, "Fail with [ "+user+" : "+passw+" ]", "CLOSE")
	else:
		logging.info('HTTPBasicAuth %s, Details=%s, %s', url, "HTTPBasicAuth Not present", "CLOSE")

def oauth_auth(url, user, passw):
	r = __get_request(url, OAuth1(user,passw))
	if __get_request(url).status_code == 401:
		if r.status_code == 200:
			logging.info('HTTPOAuth %s, Details=%s, %s', url, "Success with [ "+user+" : "+passw+" ]", "OPEN")
		else:
			logging.info('HTTPOAuth %s, Details=%s, %s', url, "Fail with [ "+user+" : "+passw+" ]", "CLOSE")
	else:
		logging.info('HTTPOAuth %s, Details=%s, %s', url, "HTTPOAuth Not present", "CLOSE")

def basic_auth(url, user, passw):
	r = __get_request(url, (user,passw))
	if __get_request(url).status_code == 401:
		if r.status_code == 200:
			logging.info('HTTP Basic Auth %s, Details=%s, %s', url, "Success with [ "+user+" : "+passw+" ]", "OPEN")
		else:
			logging.info('HTTP Basic Auth %s, Details=%s, %s', url, "Fail with [ "+user+" : "+passw+" ]", "CLOSE")
	else:
		logging.info('HTTP Basic Auth %s, Details=%s, %s', url, "HTTPBasicAuth Not present", "CLOSE")
				
def has_header_access_control_allow_origin(url):
	headers_info = __get_request(url).headers
	if 'access-control-allow-origin' in headers_info:
		value = headers_info['access-control-allow-origin']
		state = (lambda val: 'CLOSE' if re.match(regex['access-control-allow-origin'],val) != None else 'OPEN')(value)
		logging.info('%s HTTP header %s, Details=%s, %s', 'access-control-allow-origin', url, value, state)
	else:
		logging.info('%s HTTP header %s, Details=%s, %s', 'access-control-allow-origin', url, "Not Present", 'OPEN')
		
def has_header_cache_control(url):
	headers_info = __get_request(url).headers
	if 'cache-control' in headers_info:
		value = headers_info['cache-control']
		state = (lambda val: 'CLOSE' if re.match(regex['cache-control'],val) != None else 'OPEN')(value)
		logging.info('%s HTTP header %s, Details=%s, %s', 'cache-control', url, value, state)
	else:
		logging.info('%s HTTP header %s, Details=%s, %s', 'cache-control', url, "Not Present", 'OPEN')
		
def has_header_content_security_policy(url):
	headers_info = __get_request(url).headers
	if 'content-security-policy' in headers_info:
		value = headers_info['content-security-policy']
		state = (lambda val: 'CLOSE' if re.match(regex['content-security-policy'],val) != None else 'OPEN')(value)
		logging.info('%s HTTP header %s, Details=%s, %s', 'content-security-policy', url, value, state)
	else:
		logging.info('%s HTTP header %s, Details=%s, %s', 'content-security-policy', url, "Not Present", 'OPEN')
		
def has_header_content_type(url):
	headers_info = __get_request(url).headers
	if 'content-type' in headers_info:
		value = headers_info['content-type']
		state = (lambda val: 'CLOSE' if re.match(regex['content-type'],val) != None else 'OPEN')(value)
		logging.info('%s HTTP header %s, Details=%s, %s', 'content-type', url, value, state)
	else:
		logging.info('%s HTTP header %s, Details=%s, %s', 'content-type', url, "Not Present", 'OPEN')
		
def has_header_expires(url):
	headers_info = __get_request(url).headers
	if 'expires' in headers_info:
		value = headers_info['expires']
		state = (lambda val: 'CLOSE' if re.match(regex['expires'],val) != None else 'OPEN')(value)
		logging.info('%s HTTP header %s, Details=%s, %s', 'expires', url, value, state)
	else:
		logging.info('%s HTTP header %s, Details=%s, %s', 'expires', url, "Not Present", 'OPEN')
		
def has_header_pragma(url):
	headers_info = __get_request(url).headers
	if 'pragma' in headers_info:
		value = headers_info['pragma']
		state = (lambda val: 'CLOSE' if re.match(regex['pragma'],val) != None else 'OPEN')(value)
		logging.info('%s HTTP header %s, Details=%s, %s', 'pragma', url, value, state)
	else:
		logging.info('%s HTTP header %s, Details=%s, %s', 'pragma', url, "Not Present", 'OPEN')
		
def has_header_x_content_type_options(url):
	headers_info = __get_request(url).headers
	if 'x-content-type-options' in headers_info:
		value = headers_info['x-content-type-options']
		state = (lambda val: 'CLOSE' if re.match(regex['x-content-type-options'],val) != None else 'OPEN')(value)
		logging.info('%s HTTP header %s, Details=%s, %s', 'x-content-type-options', url, value, state)
	else:
		logging.info('%s HTTP header %s, Details=%s, %s', 'x-content-type-options', url, "Not Present", 'OPEN')

def has_header_x_frame_options(url):
	headers_info = __get_request(url).headers
	if 'x-frame-options' in headers_info:
		value = headers_info['x-frame-options']
		state = (lambda val: 'CLOSE' if re.match(regex['x-frame-options'],val) != None else 'OPEN')(value)
		logging.info('%s HTTP header %s, Details=%s, %s', 'x-frame-options', url, value, state)
	else:
		logging.info('%s HTTP header %s, Details=%s, %s', 'x-frame-options', url, "Not Present", 'OPEN')

def has_header_x_permitted_cross_domain_policies(url):
	headers_info = __get_request(url).headers
	if 'x-permitted-cross-domain-policies' in headers_info:
		value = headers_info['x-permitted-cross-domain-policies']		
		state = (lambda val: 'CLOSE' if re.match(regex['x-permitted-cross-domain-policies'],val) != None else 'OPEN')(value)
		logging.info('%s HTTP header %s, Details=%s, %s', 'x-permitted-cross-domain-policies', url, value, state)
	else:
		logging.info('%s HTTP header %s, Details=%s, %s', 'x-permitted-cross-domain-policies', url, "Not Present", 'OPEN')
				
def has_header_x_xxs_protection(url):
	headers_info = __get_request(url).headers
	if 'x-xss-protection' in headers_info:
		value = headers_info['x-xss-protection']
		state = (lambda val: 'CLOSE' if re.match(regex['x-xss-protection'],value) != None else 'OPEN')(value)
		logging.info('%s HTTP header %s, Details=%s, %s', 'x-xss-protection', url, value, state)
	else:
		logging.info('%s HTTP header %s, Details=%s, %s', 'x-xss-protection', url, "Not Present", 'OPEN')
