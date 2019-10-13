# project name: wrf_management
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
'''
this module tryes to make logging easier
>>> import useful_scit.util.log as log
>>> log.ger(log.log.DEBUG)
>>> log.ger.debug('leg.ger level is %s', log.log.DEBUG)
>>> log.ger.info('this message wont be shown')
>>> log.ger(log.log.INFO)
>>> log.ger.info('now this message is shown')
>>> log.ger.debug('so is this one')
>>> log.print_levels()
'''

import logging as log

log = log
ger = log.getLogger('useful_scit')
handler = log.StreamHandler()
formatter = log.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
ger.addHandler(handler)
# ger.setLevel(logging.DEBUG)

# logger.debug('often makes a very good meal of %s', 'visiting tourists')


LEVELS = [
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'FATAL'
]

def print_levels():
    for l in LEVELS:
        print(l, getattr(log, l))
