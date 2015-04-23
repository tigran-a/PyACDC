#!/usr/bin/python3

#
# Copyright SnT, University of Luxembourg
# 2014
#
# To contact authors, please, find CoSDN team in the Interdisciplinary Center of Security, Reliability and Trust (SnT), 
# at University of Luxembourg, Luxembourg.
# 

# Some simple tools for playing with urls

def url_join(*args):
	""" joins arguments as parts of url using '/' as a separator """ 
	res = args[0]
	for a in args[1:]:
		if a is not None and a != '':
			res = res.rstrip('/') + '/' + a.lstrip('/')
	return res

def build_base_url(scheme='https', host = 'localhost', port = None, path = '/'):
	assert host is not None and host !=''
	assert path is not None
	sep = '/'
	if path == '' or path.startswith('/'):
		sep = ''

	return scheme + '://' + host + ((":"+str(port)) if port is not None else '') + sep + path
