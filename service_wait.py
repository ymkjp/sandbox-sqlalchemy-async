import tornado.ioloop
import tornado.web
import json
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tornado.web import RequestHandler,asynchronous 
import threading

class Worker(threading.Thread):
    def __init__(self, callback=None, wait=5, *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)
        self.callback = callback
        self.wait = wait
            
    def run(self):
        print "wait start"
        time.sleep(self.wait)
        print "wait end"
        self.callback(self.wait)


class MainHandler(tornado.web.RequestHandler):
    @asynchronous
    def get(self):
        wait = float(self.get_arguments('wait')[0])
        result = 'wait time %i ' % wait
        Worker(self.worker_done,wait=wait).start()
        #self.write(result)
        #self.finish()

    def worker_done(self, value):
        print "callback called"
        self.write("end")
        self.finish()


application = tornado.web.Application([ (r"/wait",MainHandler), ])

if __name__ == "__main__": 
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
