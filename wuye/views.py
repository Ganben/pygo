from django.shortcuts import render
from django.views import View
import requests, json, random
from .config import nogit
from django.core.cache import caches  # per thread use cache
import logging, datetime, time
import string, hashlib

# Create your views here.

# the cached objects for wx-js-sdks:
# access token

WX_API_Base = 'https://api.weixin.qq.com/cgi-bin/token?grant_type={0}&appid={1}&secret={2}'
WX_API_AccessToken = WX_API_Base.format('client_credential', nogit.wxTestAppID, nogit.wxTestAppSecret)

WX_API_Ticket = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=jsapi'

logger = logging.getLogger('django')

def get_jsapi_sign(for_url):   #return a struct of jsapi needed data
	logging.debug('----------------------- start get jsapi_ticket')
	cache = caches['default']

	if cache.get('access_token') == None: #if token expired, return None and renew fetch
		res =  requests.get(WX_API_AccessToken)
		logger.debug('res access_token content = {0}'.format(str(res.content)))
		data = {}
		try:
			data.update(json.loads(res.text))
		except:
			logger.warn('access token ------------ parse json error')
		cache.set('access_token', data.get('access_token'), 7200)

	# else:
	access_token = cache.get('access_token')

	if cache.get('jsapi_ticket') == None:
		res = requests.get(WX_API_Ticket.format(access_token))
		logger.debug('res jsapi content = {0}'.format(str(res.content)))
		data = {}
		try:
			data.update(json.loads(res.text))
		except:
			logger.warn('jsapi parse  -------------- json error')
		cache.set('jsapi_ticket', data.get('ticket'), 7200)

	jsapi_ticket = cache.get('jsapi_ticket')

	noncestr = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)]) #len = 32 random string

	# appId = nogit.wxTestAppID
	timestamp = int(time.time())
	url = for_url
	m = hashlib.sha1()
	s4sig = 'jsapi_ticket={0}&noncestr={1}&timestamp={2}&url={3}'.format(jsapi_ticket,noncestr,timestamp,url)
	logger.debug('gen str 4 sig = {0}'.format(s4sig))
	m.update(s4sig)
	signature = m.digest()
	logger.debug('signature is {0}'.format(signature))
	configdata = {}
	configdata.update({'appId': nogit.wxTestAppID})
	configdata.update({'timstamp': timestamp})
	configdata.update({'nonceStr': noncestr})
	configdata.update({'signature': signature})

	return configdata

