import os
import time, datetime
import logging

def redirect_log(root=None):
    log_file_name = ''
    now_time = datetime.datetime.now()
    if not os.path.exists(os.path.join(root, 'log/%s' % str(now_time.year))):
        os.mkdir(os.path.join(root, 'log/%s' % str(now_time.year)))
    if not os.path.exists(os.path.join(root, 'log/%s/%02d' % (str(now_time.year), now_time.month))):
        os.mkdir(os.path.join(root, 'log/%s/%02d' % (str(now_time.year), now_time.month)))
        
    time_flag = time.strftime("%Y_%m_%d", now_time.timetuple())
    log_file_name = os.path.join(root, 'log/%s/%02d/app.%s.log' % (str(now_time.year), now_time.month, time_flag))
    assert log_file_name <> ''
    return log_file_name

def locate_file_log(root=None):
    log_file = redirect_log(root)
    print log_file
    handler = logging.FileHandler(filename=log_file, mode='a', encoding='utf8', delay=True)
    formatter = logging.Formatter('[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)

def locate_console_log():
    import tornado.options
    tornado.options.enable_pretty_logging()
