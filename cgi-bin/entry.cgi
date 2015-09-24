#!/usr/local/bin/python
#coding:utf-8

import cgitb
import os
cgitb.enable()
import Cookie
import datetime
import pickle


NAME_DBFILE = "cgi-bin/name_file.dump"
ROUTINE_DBFILE = "cgi-bin/routine_file.dump"

def kaitou(filename):
    f = open(filename,"r")
    name_list = pickle.load(f)
    f.close()
    return name_list

def changeStringToDatetime(str_data):
    """
    strのフォーマットはyear/month/day/hour/minute/second
    """
    a = str_data.split("/")
    a = list(map(int,a))
    return datetime.datetime(*a)


def changeDatetimeToString(date,num):
    y = date.year
    m = date.month
    d = date.day
    h = date.hour
    mi = date.minute
    s = date.second

    if num == 3:
        return "%s/%s/%s"%(y,m,d)
    else:
        return "%s/%s/%s/%s/%s/%s"%(y,m,d,h,mi,s)

fail_page = '''Content-Type: text/html

<html>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>アクセス権限がありません</title>
</head>

<body>
    <h1>編集画面にアクセスするにはログインをしてください</h1><br>
    <a href="http://0.0.0.0:8000/cgi-bin/login.cgi">ログイン画面</a>
</body>

</html>
'''

ok_page = '''Content-Type: text/html

<html>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>編集画面</title>
</head>

<body>
    <CENTER>
    <h1>ここは編集画面トップページです</h1>
    <a href="http://0.0.0.0:8000/cgi-bin/logout.cgi">ログアウト</a><br>
    <a href="http://0.0.0.0:8000/cgi-bin/addperson.cgi">人の登録</a><br>
    <a href="http://0.0.0.0:8000/cgi-bin/addroutine.cgi">ルーチンの登録</a>

    <p>
        %s
    </p>
    </CENTER>
</body>

</html>
'''

if 1:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c=Cookie.SimpleCookie()
    c.load(cookie_string)
    if c["login"].value == "ok":
        name_dict = kaitou(NAME_DBFILE) #名前と登録日の辞書
        routine_dict = kaitou(ROUTINE_DBFILE) #ルーチンワークの辞書
        now = datetime.datetime.now()

        tmp = ""
        for name, date in name_dict.values():
            day = (now - changeStringToDatetime(date)).days
            if day in routine_dict.keys():
                tmp += "%sさん ->『%s』を行う必要があります<br>"%(name, routine_dict[day][1])

        print ok_page%tmp

    else:
        print fail_page

else:
    print fail_page