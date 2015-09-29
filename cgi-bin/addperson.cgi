#!/usr/local/bin/python
#coding:utf-8

from __future__ import with_statement
import fcntl
import cgi
import cgitb
import os
cgitb.enable()
import Cookie
import pickle
import uuid
from datetime import datetime

DBFILE = "cgi-bin/name_file.dump"

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

def kaitou(filename):
    #排他制御
    with open(filename,"r") as l_file:
        fcntl.flock(l_file.fileno(), fcntl.LOCK_EX)
        name_list = pickle.load(l_file)

    return name_list

def kakikomi(dict_name):
    #排他制御
    with open(DBFILE,"w") as l_file:
        fcntl.flock(l_file.fileno(), fcntl.LOCK_EX)
        pickle.dump(dict_name, f)

def returnNames(name_list):
    tmp = ""
    for i, n in enumerate(name_list.keys()):
        tmp += name_list[n][0] + "さん(%s)"%(name_list[n][1]+"に追加")+'<input type="submit" name="%s" value="削除" />'%n+"<br>"
    return tmp


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
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1/jquery-ui.min.js"></script>
    <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1/i18n/jquery.ui.datepicker-ja.min.js"></script>
    <link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1/themes/redmond/jquery-ui.css" >
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>人の登録ページ</title>

    <script>
        $(function() {
            $("#datepicker").datepicker();
        });

        function check(){
            var now = new Date(); //今の日付
            var date = new Date($("#datepicker").val()); //入力された日付
            var name = $("#name").val();
            var msDiff = now.getTime() - date.getTime(); 
            var daysDiff = Math.floor(msDiff / (1000 * 60 * 60 *24));

            if(daysDiff >= 1){
                if(window.confirm(name+"さんの日付は既に"+daysDiff+"日経っていますが本日の日付に変更しますか？")){
                    var tmp = now.getFullYear()+"/"+now.getMonth()+"/"+now.getDate()
                    document.getElementById("datepicker").value = tmp;
                }
                else{
                    window.alert("入力された日付で登録されました");
                }
            }
            return true;
        }
    </script>

</head>

<body>
    <CENTER>
    <h1>ここは人を登録するページです</h1>
    <a href="http://0.0.0.0:8000/cgi-bin/entry.cgi">トップページに戻る</a>

    <form action="addperson.cgi" method="post" onSubmit="return check()">
        <p>
            本人を知った日付<input type="text" id="datepicker" name="datepicker"><br>
            <font color="red">※省略された場合は本日の日付になります</font>
        </p>
        お名前<input type="text" name="name" id="name" /><br>
        <input type="submit" value="追加"/>
    </form>

    <h4>現在追加されている方々</h4>
    <form action="addperson.cgi" method="post">
       %s
    </form>
    </CENTER>
</body>

</html>
'''

if 1:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c=Cookie.SimpleCookie()
    c.load(cookie_string)

    if 1: #ログインが確認できたら
        field = cgi.FieldStorage()
        name = cgi.escape(field.getfirst("name", ""), True)
        date = cgi.escape(field.getfirst("datepicker", changeDatetimeToString(datetime.now, 3)),
                          True)

        try: #人の名前を削除
            name_list = kaitou()

            for k in name_list.keys():
                if field.getfirst(k):
                    del name_list[k]
            kakikomi(name_list)

        except: #削除途中で例外発生
            kakikomi(name_list)
            pass

        try: #テキストファイルに名前のリストを保存
            name_list = kaitou()

            if name != "" and date != "": #もし名前が入力されていたら
                name_list[str(uuid.uuid4())] = [name,date]
                kakikomi(name_list)
                print ok_page%returnNames(name_list)

            else: #名前が入力されていなかったら
                print ok_page%returnNames(name_list)

        except: #テキストファイルに名前のリストを保存が失敗したら
            print ok_page%""

    else: #ログインが確認できなかったら
        print fail_page

else: #Cookieが無かったら
    print fail_page