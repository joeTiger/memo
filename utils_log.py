import logging
import sys

#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
#logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL)

def set_log_level(level='debug'):
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    if level == 'debug':
        logging.basicConfig(
            stream=sys.stderr,
            level=logging.DEBUG,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(threadName)s: %(message)s', #  %(module)s - %(funcName)s %(thread)d
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL)

    logging.debug('level log is {}...'.format(level))


def log_debug(s):
    logging.debug(s)


def log_critical(s):
    logging.critical(s)


def log_info(s):
    logging.info(s)
