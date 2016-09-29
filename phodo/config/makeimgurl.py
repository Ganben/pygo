#-*- coding: utf-8 -*-
# ganben created

from uuid import uuid1
import time, os, logging

logger = logging.getLogger('django')

def imagename(file):
	ext = file.name.split('.')[-1]
	return '{0}{1}.{ext}'.format(time.strftime("%Y/%m/"), uuid1(), ext=ext)

def maketxt(o_id, s):
	f = open('%s.txt' % o_id, 'w')
	f.write(s)
	f.close()
	logger.debug('make txt success for {0}'.format(o_id))
	return '%s.txt' % o_id

def deletetxt(o_id):
	if os.path.isfile('%s.txt' % o_id):
		try:
			os.remove('%s.txt' % o_id)
			logger.debug(('rm txt'))
			return True
		except:
			return False
	else:
		return False

def uploadImgHandler(uplfile):
	ext = uplfile.name.split('.')[-1]
	size = uplfile.size
	if ext == 'jpg':
		if size <= 2048000:
			return uplfile.read()

	logger.debug('file not jpg or too big')
	return False
