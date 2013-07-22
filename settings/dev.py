# -*- coding: utf-8 -*-

from settings.common import *

########## DEBUG CONFIGURATION
DEBUG = True
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION

LOGGING['loggers'].update({
        'pinger': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
})