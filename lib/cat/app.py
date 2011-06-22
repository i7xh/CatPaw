import optparse
import os, sys
import logging

def run(root=None):
    opt = optparse.OptionParser()
    opt.add_option('--loglevel', '-l', default='notset', help='logging level: notset, debug, info, warning, error')
    opt.add_option('--daemon', '-d', action='store_true', help='mode: console, daemon')
    opt.add_option('--port', '-p', default=8000, help='web port')
    options, arguments = opt.parse_args()
    print options
    print arguments
    
    if 'shell' in arguments:
        import code
        code.interact()
        sys.exit(1)
    if options.daemon:
        from utils.xlogger import locate_file_log 
        locate_file_log(root)
    else:
        from utils.xlogger import locate_console_log
        locate_console_log()
    
    logging.getLogger().setLevel(getattr(logging, options.loglevel.upper()))
    logger = logging.getLogger()
    
    logger.debug('start xoo app...')
    logger.info('start xoo app...')
    logger.warning('start xoo app...')
    logger.error('start xoo app...')
    logger.fatal('start xoo app...')
    
    port = options.port
    if options.daemon: 
        action = arguments[0]
        from utils.xDaemon import run_daemon
        run_daemon(root, action, port)
    else:
        from utils.xConsole import run_console
        run_console(port)

