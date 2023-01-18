import logging
import logging.config


def configure_logger(name):
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'WARNING',
                'propagate': False
            },
            'lenta': {
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': False
            }
        }
    })
    return logging.getLogger(name)
