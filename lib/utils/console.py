import tornado.httpserver
import tornado.ioloop 
import tornado.web
import logging
from xoo.xApp import Xoo

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/test',TestHandler),
            ]
        settings = dict(
            #template_path=os.path.join(os.path.dirname(__file__), "templates"),
            #static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        logging.info('create application')
        tornado.web.Application.__init__(self, handlers, **settings)

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('test...')

def run_console(port):
    logging.info('run_console...')
    http_server = tornado.httpserver.HTTPServer(Xoo(), xheaders=False)
    http_server.listen(int(port))
    tornado.ioloop.IOLoop.instance().start()
