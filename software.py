#!/usr/bin/python3
# -*- utf-8 -*-
#   Copyright (C) 2021,2022 Ken'ichi Fukamachi, all rights reserved. see ./LICENSE file.
#
# based on the www.py of the exercises in the lecture "operating system"
#   https://exercises-aws.fml.org/ja/04_docker/04-04_debian-nginx-web.py-mysql/docker/files/var/www/libexec/www.py
#

import os
import sys
import http.server
import socketserver
import cgi
import random
import os



#
# Configurations
#
HTTP_HOST       = "0.0.0.0"
HTTP_PORT       = 80


#
#   WWW server example: Handler class, which handles www requests
#

# Handler   = http.server.SimpleHTTPRequestHandler
class Handler(http.server.SimpleHTTPRequestHandler):
   def __init__(self, *args, **kwargs):
      sudo_user = os.environ['SUDO_USER']    # ec2-user
      home_dir  = "/home/" + sudo_user       # /home/ec2-user
      user_dir  = home_dir + "/public_html"  # ~/public_html/
      super().__init__(*args, directory=user_dir, **kwargs)

   def _set_headers(self):
      self.send_response(200)
      self.send_header('Content-type','text/html; charset=utf-8')
      self.end_headers()

   def do_GET(self):
      
    return self.__hello_world()

   def __hello_world(self):
    # -*- coding: utf-8 -*-
    import re
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn import linear_model,ensemble,tree
    
    #平均気温(℃)  降水量の合計(mm)  日照時間(時間)    最深積雪(cm)    平均風速(m/s)   最高気温(℃)   最低気温(℃)
    #データファイルを開く
    f=open('data.csv','r')
    d=re.split('[,\n]',f.read())
    f.close()
    
    #目的変数の配列を作成する
    target=[]
    for i in d[0::5]:
        target.append(i)
    del target[-1]
    
    #目的変数に対応する要素を消す
    del d[::5]
    
    #NumPy配列を作成する
    d = np.array(d, dtype='float64')
    target = np.array(target, dtype='float64')
    
    #説明変数(2次元)を作成する
    data=d.reshape(int(len(d)/4),4)
    
    #明日の予測を出すために説明変数の最初の要素だけ消す
    data=np.delete(data,len(target)-1,0)
    #明日の予測を出すために目的変数の最後の要素だけ消す
    target=np.delete(target,-1)
    
    #学習用データとテスト用データで分ける
    traind, testd, traint, testt =train_test_split(data,target, test_size=0.2)
    
    #AIモデルを作成する
    clf = ensemble.BaggingRegressor(tree.DecisionTreeRegressor(), n_estimators=100, max_samples=0.3)
    #学習させる
    clf.fit (traind,traint)
    
    print('スコア:'+str(clf.score(testd,testt)))
    
    #ある日の 降水量の合計(mm),日照時間(時間),最深積雪(cm),平均風速(m/s) のデータ
    t=[[0,3.8,1,1]]
    #予測値の算出
    pre = clf.predict(t)
    print(pre)
            
    def do_POST(self):
      self._set_headers()
      form = cgi.FieldStorage(
         fp=self.rfile,
         headers=self.headers,
         environ={'REQUEST_METHOD': 'POST'}
      )
      reply = self.__janken(form)
      self.wfile.write(bytes(reply, "utf8"))

    def __janken(self, form):
      janken  = Janken(form)
      kekka   = janken.kekka()
      message = "<html><body> {} </body></html>\n".format(kekka)
      return message


# [JANKEN SPEC] 0 = GUU, 1 = CHOKI, 2 = PAA      
# variables: jibun (user), aite (computer), kekka
class Janken():
   def __init__(self, form):
      self.form    = form

   def jibun(self):
      return int(self.form.getvalue("jibun", -1))
   
   def aite(self):
      return int(random.randint(0, 2))

   def kekka(self):
      te_romaji    = { 0:'guu',  1:'choki', 2:'paa'   }
      kekka_romaji = { 0:'aiko', 1:'make',  2:'kachi' }
      te_jibun     = self.jibun()
      te_aite      = self.aite()
      _kekka       = (3 + te_jibun - te_aite ) % 3
      jibun_romaji = te_romaji[ te_jibun ]
      aite_romaji  = te_romaji[ te_aite ]
      kekka_romaji = kekka_romaji[ _kekka ]
      return "[{},{},{}] # jibun = {}, aite = {}, kekka = {}".format(te_jibun, te_aite, _kekka, jibun_romaji, aite_romaji, kekka_romaji)


#
# MAIN
#
if __name__ == "__main__":
   # version 3 only
   if sys.version_info.major < 3:
      print("***error: python 2 is not supported")
      sys.exit(1)

   # run python www server (httpd)
   with socketserver.TCPServer((HTTP_HOST, HTTP_PORT), Handler) as httpd:
      print("(debug) serving at port", HTTP_PORT)
      httpd.serve_forever()