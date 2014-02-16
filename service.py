import tornado.ioloop
import tornado.web
import json
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tornado.web import RequestHandler,asynchronous 
import threading

class Worker(threading.Thread):
    def __init__(self, callback=None, *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)
        self.callback = callback

    def run(self):
        time.sleep(10)
        self.callback('DONE')

class SqlAlchemyHandler(tornado.web.RequestHandler):
    def initialize(self):
        engine = create_engine('postgresql://sugino:bigbird@localhost:5432/sugino')
        self.conn = engine.connect()
        Session = sessionmaker(bind=engine)
        Session.configure(bind=engine)
        session = Session()
            
class MainHandler(SqlAlchemyHandler):
    #@asynchronous
    def get(self):
        Worker(self.worker_done)

    def worker_done(self, value):
#        _ = dict()
#        self.conn.execute('unlock table dc')
#        _['id'] = "11111"
#        _['name'] = 'BHEC Yokohama'
#        j = json.dumps(_)
#        self.write(j)
#        self.finish(value)

        rows=self.conn.execute('lock table dc')
        sql = 'select * from dc'
        rows=self.conn.execute(sql)
        result=''
        for r in rows:
            result += r[0] + '\n'

        self.write(result)
        self.finish()


application = tornado.web.Application([ (r"/dc",MainHandler), ])

if __name__ == "__main__": 
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
