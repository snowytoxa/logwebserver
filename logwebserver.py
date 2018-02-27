#!/usr/bin/env python3
'''
Simple webserver that stores POST requests and let you browse it
'''
from datetime import datetime
import logging
import os
import os.path
import tempfile
import warnings
from flask import Flask, request, make_response # pylint: disable=import-error
from flask.exthook import ExtDeprecationWarning # pylint: disable=import-error

warnings.simplefilter('ignore', ExtDeprecationWarning)

from flask_autoindex import AutoIndex # pylint: disable=import-error,wrong-import-position

LOG_LEVEL = logging.INFO
logging.basicConfig(level=LOG_LEVEL,
                    format='%(asctime)s %(levelname)s %(name)s: %(message)s')
LOG = logging.getLogger(__name__)

LOGS_DIR = tempfile.mkdtemp()
FLASK_APP = Flask(__name__)
AutoIndex(FLASK_APP, browse_root=LOGS_DIR)


@FLASK_APP.errorhandler(405)
def log_post(e):
    '''
    Function will log all incoming POST requests
        Args:
            e (code or exception): exception
        Returns:
            str: always returns "OK"
    '''
    if request.method == 'POST':
        path = request.path
        logfile = os.path.join(LOGS_DIR,\
            os.path.join(path,\
                datetime.now().isoformat()).replace('/', '_'))
        if request.is_json:
            data = request.data
            open(logfile + '.json', 'wb').write(data)
        else:
            data = request.stream.read()
            open(logfile + '.bin', 'wb').write(data)
        return 'OK %d'%(len(data))
    return make_response(e)


if __name__ == '__main__':
    LOG.info('Will store all files into %s', LOGS_DIR)
    FLASK_APP.run()
