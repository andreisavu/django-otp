""" 
One Time password generator
"""

import settings, random

def id(channel='', length=settings.PASWD_LENGTH):
    d = '1234567890'
    return ''.join([random.choice(d) for x in range(1,length)])

