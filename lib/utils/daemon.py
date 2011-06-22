#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, os, time, atexit
from signal import SIGTERM
from decorator import Retry
import tornado.httpserver
import tornado.ioloop
import tornado.web
import logging
from xoo.xApp import Xoo

def run_daemon(root, action, port):
    tmp_path = os.path.join(root, 'tmp')
    pidfile = os.path.join(tmp_path, 'pids/eclipse.%s.pid' % port)
    daemon = xDaemon(pidfile=pidfile, stdout='/dev/null', stderr='/dev/null', port=port) 
    logging.info('run_daemon....')
    if action.lower() == "start": logging.info('start...'); daemon.start()
    elif action.lower() == "stop": logging.info("stop..."); daemon.stop()
    elif action.lower() == "restart": logging.info("restart"); daemon.restart()
    else:
        logging.info('invalid arguments!')
        sys.exit(2)
    sys.exit(0)

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

class Daemon:
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        #父进程自杀
        try:
            pid = os.fork()
            if pid > 0:
                #exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        #拷贝父进程的运行环境
        os.chdir(".")
        os.setsid()
        os.umask(0)
        
        #拷贝父进程的运行环境
        #第二次fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        #重定向日志输出
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        self.daemonize()
        self.run()

    def stop(self):
        """
        stop the daemon
        """
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return

        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                else:
                    print str(err)
                    sys.exit(1)

    def restart(self):
        """
        restart the App
        """
        self.stop()
        print "restart the server"
        #self.stdout.write("restart the App")
        self.start()

    def run(self):
        """
        inherit class override this method!
        """
        pass

    @Retry(3)
    def demo(self, retry):
        print "i am illed"
        print s
        return -1

    def test(self):
        r = self.demo()
    
    
class xDaemon(Daemon):
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', port=8000):
        Daemon.__init__(self, pidfile, stdin, stdout, stderr)
        import logging
        logging.info('120')
        self.port = port
    """
    override server run
    """
    #@Retry(Exception, phoenix=False, tries=4)
    def run(self):
        http_server = tornado.httpserver.HTTPServer(Xoo())
        http_server.listen(int(self.port))
        tornado.ioloop.IOLoop.instance().start()

    
if __name__ == "__main__":
    daemon = Daemon('./test.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'test' == sys.argv[1]:
            daemon.test()
        else:
            print 'Unknown Command'
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start | stop | restart" % sys.argv[0]
        sys.exit(2)

