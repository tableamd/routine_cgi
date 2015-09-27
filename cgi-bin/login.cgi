#!/usr/local/bin/python
#coding:utf-8

import cgi
import cgitb
import os
cgitb.enable()
import Cookie

USERNAME = "username"
PASSWORD = "password"

login_page = '''Content-Type: text/html

<html>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>ログイン画面</title>
</head>

<body>
	<CENTER>
	<h1>ログインしてください</h1>
	<form action="login.cgi" method="post">
		<p>ユーザ名<input type="text" name="username" /></p>
		<p>パスワード<input type="password" name="password" /></p>
		<input type="submit" value="ログイン"/>
	</form>
	</CENTER>
</body>

</html>
'''


f = cgi.FieldStorage()
username = cgi.escape(f.getfirst("username", ""),True)
password = cgi.escape(f.getfirst("password", ""),True)


if username != USERNAME or password != PASSWORD:
    print login_page
else:
    sc=Cookie.SimpleCookie()
    sc['login']="ok"
    print sc
    print "Location: http://0.0.0.0:8000/cgi-bin/entry.cgi\n\n"





