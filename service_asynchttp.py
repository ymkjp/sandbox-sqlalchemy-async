import tornado.ioloop
import tornado.web
import json
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler,asynchronous 
import tornado.httpclient
import threading
import logging

class MainHandler(tornado.web.RequestHandler):

    @asynchronous
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = client.fetch("http://localhost:8888/wait?wait=10", self.handle_request)

    def handle_request(self,response):
        if response.error:
            print "Error:", response.error
        self.write("end")
        self.finish()



application = tornado.web.Application([ (r"/dc",MainHandler), ])

if __name__ == "__main__": 
    application.listen(8887)
    tornado.ioloop.IOLoop.instance().start()
