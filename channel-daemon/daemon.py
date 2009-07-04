#! /usr/bin/env python
"""
Message gateway server for django otp

Implemented send methods:
    smtp - to:

"""

from SimpleXMLRPCServer import SimpleXMLRPCServer
import settings, sys

def gen_id(n):
    d = '1234567890'
    import random
    return ''.join([random.choice(d) for x in range(1,n)])

def send_with_id(channel, params):
    return send(channel, "Your one time password is: %s" % gen_id(settings.PASWD_LENGTH), params)    

def send(channel, msg, params):
    if channel == 'smtp':
        return send_smtp(msg, params)
  
    return False

def send_smtp(msg, params):
    import mail
    mail.send(serverURL=settings.SMTP['server'], 
        sender=settings.SMTP['sender'],
        to=params['to'],
        subject=settings.SMTP['subject'],
        text=msg)
    return True

def main(argv):
    port = 8000
    if len(argv) > 1:
        port = int(argv[1])

    server = SimpleXMLRPCServer(('', port))
    server.register_introspection_functions()
    
    server.register_function(send, 'send')
    server.register_function(send_with_id, 'send_with_id')

    print "Starting server on port %d ..." % port
    try:
        server.serve_forever()
    except KeyboardInterrupt, e:
        print "Good bye."

if __name__ == '__main__':
    main(sys.argv)
