#!/usr/local/bin/python
#coding:utf-8

import cgi
import cgitb
import os
cgitb.enable()
import Cookie
import pickle

DBFILE = "cgi-bin/routine_file.dump"

def kaitou():
    f = open(DBFILE,"r")
    name_list = pickle.load(f)
    f.close()
    return name_list

def kakikomi(dict_name):
    f = open(DBFILE,"w")
    pickle.dump(dict_name, f)
    f.close()


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
    <title>ルーチンワーク登録ページ</title>

    <script type="text/javascript">
        function checkSubmit() {
            //return confirm(document.form1.work.value);
            var y = document.getElementById("year");
            var work = document.getElementById("work2"); 
            if(window.confirm("送信してよろしいですか？"+work.value+y.value)){ // 確認ダイアログを表示
                //work.value = "hogehoge";
                return true; // 「OK」時は送信を実行

            }
            else{ // 「キャンセル」時の処理
                window.alert("キャンセルされました"); // 警告ダイアログを表示
                return false; // 送信を中止
            }
        }
    </script>
</head>
<body>
    <CENTER>
    <h1>ここはルーチンワークを登録するページです</h1>
    <a href="http://0.0.0.0:8000/cgi-bin/entry.cgi">トップページに戻る</a>

    <form action="addroutine.cgi" method="post" id="form1" onSubmit="return checkSubmit()">
        登録から
        <input type="number" name="year" id="year" min="0" style="width:60px;" value="0">年
        <input type="number" name="month" min="0" style="width:60px;" value="0">ヶ月
        <input type="number" name="week" min="0" style="width:60px;" value="0">週
        <input type="number" name="day" min="0" style="width:60px;" value="0">日 後に
        <input type="text" name="work" id="work2" style="width:200px;">をする
        <input type="submit" value="追加"/>
    </form>

    <h4>現在追加されている方々</h4>
    <form action="addroutine.cgi" method="post">
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

    if 1:
        #print ok_page
        field = cgi.FieldStorage()
        y = int(field.getfirst("year", -1))
        m = int(field.getfirst("month", -1))
        w = int(field.getfirst("week", -1))
        d = int(field.getfirst("day", -1))
        work = field.getfirst("work", "")

        r_dict = kaitou()
        for val in r_dict.keys():
            if field.getfirst("btn%d"%val):
                del r_dict[val]
        kakikomi(r_dict)


        r_dict = kaitou()

        if ((y != -1) or (m != -1) or (w != -1) or (d != -1)) and work != "":
            days = y*365 + m*30 + w*7 + d
            r_dict[days] = ["%d年%dヶ月%d週%d日後"%(y,m,w,d), work]
            kakikomi(r_dict)
            r_keys = r_dict.keys()
            r_keys.sort()

            tmp = ""
            for k in r_keys:
                tmp += "%d日後(%s)に %s をする"%(k, r_dict[k][0], r_dict[k][1])+'<input type="submit" name="btn%d" value="削除" /><br>'%k

            print ok_page%tmp

        else:
            r_dict = kaitou()
            r_keys = r_dict.keys()
            r_keys.sort()

            tmp = ""
            for k in r_keys:
                tmp += "%d日後(%s)に %s をする"%(k, r_dict[k][0], r_dict[k][1])+'<input type="submit" name="btn%d" value="削除" /><br>'%k

            print ok_page%tmp

    else:
        print fail_page

else:
    print fail_page