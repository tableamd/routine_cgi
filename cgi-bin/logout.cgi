#!/usr/local/bin/python
#coding:utf-8

import cgitb
import os
cgitb.enable()
import Cookie

if 1:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)

	if 1:
		c["login"] = ""

		print c
		print "Location: http://0.0.0.0:8000/cgi-bin/login.cgi\n\n"
	else:
		print "Content-Type: text/html"
		print
		print "this action is not allowed."
else:
	print "Content-Type: text/html"
	print
	print "this action is not allowed."