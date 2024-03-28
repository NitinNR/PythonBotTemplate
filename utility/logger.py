import logging
logging.basicConfig(filename='logs/*.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',datefmt='%Y-%m-%d %H:%M:%S%z')
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('google.auth._default').setLevel(logging.WARNING)
logging.getLogger('sqlitedict').setLevel(logging.WARNING)
logging.getLogger('google.auth.transport.requests').setLevel(logging.WARNING)

def show(msg):
    logging.debug(msg)
