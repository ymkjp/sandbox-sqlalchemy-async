import tornado.ioloop
import tornado.web
import json
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session, relationship
from tornado.web import RequestHandler,asynchronous 
from sqlalchemy.ext.declarative import declarative_base
import threading

from psyco_gevent import make_psycopg_green
import gevent
class Worker(threading.Thread):
    def __init__(self, callback=None, *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)
        self.callback = callback

    def run(self):
        time.sleep(10)
        self.callback('DONE')

Base = declarative_base()
def runit( self):
    engine = self.db
    sess = Session(engine)
    sess.execute("SELECT pg_sleep(3)")
    self.write("end")
    self.finish()

class SqlAlchemyHandler(tornado.web.RequestHandler):
    def initialize(self):
#        sqlalchemy.dialects.registry.register("postgresql", "sqlalchemy_gevent", "PostgreSQLDialect")
        from sqlalchemy.pool import NullPool
        engine = create_engine('postgresql+psycopg2://sugino:bigbird@localhost/sugino', 
                                echo=True, 
                                poolclass=NullPool
                                )

        make_psycopg_green()

        #self.conn = engine.connect()
        #Session = sessionmaker(bind=engine)
        #Session.configure(bind=engine)
        #session = Session()
        self.db = engine
            
class MainHandler(SqlAlchemyHandler):
    @asynchronous
    def get(self):

        t = gevent.spawn(runit, self)
        t.join()
        #threads = [gevent.spawn(runit, self.db) for i in xrange(1)]
        #fkor t in threads:
        #    t.join()

    def worker_done(self, value):
        _ = dict()
        self.write(vale)
        self.finish()



application = tornado.web.Application([ (r"/dc",MainHandler), ])

if __name__ == "__main__": 
    application.listen(9888)
    tornado.ioloop.IOLoop.instance().start()
