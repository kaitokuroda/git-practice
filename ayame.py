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
    from sklearn import datasets
    iris = datasets.load_iris() #irisデータセットの読み込み
    X = iris.data #訓練/テストデータ
    Y = iris.target #教師データ
    iris.feature_names
    from sklearn.model_selection import ShuffleSplit
    ss = ShuffleSplit(train_size=0.5, test_size=0.5, random_state=0)
    train_index, test_index = next(ss.split(X))
    X_train, Y_train = X[train_index], Y[train_index] #訓練データ
    X_test, Y_test = X[test_index], Y[test_index] #テストデータ
    next(ss.split(X))
    from sklearn import svm
    lng = svm.SVC()
    lng.fit(X_train, Y_train)
    print(lng.score(X_test, Y_test))
    message = str(lng.score(X_test, Y_test))
    self.wfile.write(bytes(message, "utf8"))
    

if __name__ == "__main__":
   # version 3 only
   if sys.version_info.major < 3:
      print("***error: python 2 is not supported")
      sys.exit(1)

   # run python www server (httpd)
   with socketserver.TCPServer((HTTP_HOST, HTTP_PORT), Handler) as httpd:
      print("(debug) serving at port", HTTP_PORT)
      httpd.serve_forever()
