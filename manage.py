# coding:utf8
from app import app

# 1 git reset --hard
# 2 git pull
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
if __name__=="__main__":
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8081)  #flask默认的端口
    IOLoop.instance().start()
