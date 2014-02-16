from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado.web import *

import psycopg2
import momoko


class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db


class TutorialHandler(BaseHandler):

    def _done(self, cursor, error):
        self.write('Results: %r' % (cursor.fetchall(),))
        self.finish()

    @asynchronous
    #@gen.engine
    def get(self):
        self.db.execute("select * from dc", callback=self._done)


if __name__ == '__main__':
    parse_command_line()
    application = Application([
        (r'/', TutorialHandler)
    ], debug=True)

    application.db = momoko.Pool(
        dsn='dbname=sugino  user=sugino password=bigbird'
            'host=localhost port=5432',
        size=10
    )

    http_server = HTTPServer(application)
    http_server.listen(8888, 'localhost')
    IOLoop.instance().start()
