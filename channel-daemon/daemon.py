#! /usr/bin/env python
"""
Message gateway server for django otp

Implemented send methods:
    smtp - to:

"""

from SimpleXMLRPCServer import SimpleXMLRPCServer
import settings, generator
import sys,os,xmpp,time

def send_id(channel, params):
    id = generator.id(channel)
    msg = "Your one time password is: %s" % id
    if not send(channel, msg, params):
        return False
    return id

def send(channel, msg, params):
    if channel == 'smtp':
        return send_smtp(msg, params)
    elif channel == 'im':
        return send_im(msg, params)
    return False

def send_smtp(msg, params):
    import mail
    mail.send(serverURL=settings.SMTP['server'], 
        sender=settings.SMTP['sender'],
        to=params['to'],
        subject=settings.SMTP['subject'],
        text=msg)
    return True

def send_im(msg, params):
    jid = xmpp.protocol.JID(settings.XMPP['jid'])
    cl = xmpp.Client(jid.getDomain(),debug=[])
    con = cl.connect()
    if not con:
        return False
    auth=cl.auth(jid.getNode(), settings.XMPP['passwd'], resource=jid.getResource())
    if not auth:
        return False
    id=cl.send(xmpp.protocol.Message(params['to'], msg))
    time.sleep(1)
    cl.disconnect()
    return True

def get_channels():
    return [{
        'id':'smtp',
        'name':'Email',
        'description':'Use an email address for receiving the password',
        'params':{'to':'Adresa'}
        },{
        'id':'im',
        'name':'Jabber/XMPP',
        'description':'Use a jabber/IM account',
        'params':{'to':'Username'}
        }]

def main(argv):
    port = 8000
    if len(argv) > 1:
        port = int(argv[1])

    server = SimpleXMLRPCServer(('', port))
    server.register_introspection_functions()
    
    server.register_function(send, 'send')
    server.register_function(send_id, 'send_id')
    server.register_function(get_channels, 'get_channels')

    print "Starting server on port %d ..." % port
    try:
        server.serve_forever()
    except KeyboardInterrupt, e:
        print "Good bye."

if __name__ == '__main__':
    main(sys.argv)

