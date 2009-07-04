#! /usr/bin/env python
"""
Message gateway server for django-otp

Implemented send methods:
    smtp - to:  email address
    im   - to:  user@jabber-server
    sms  - to:  phone number

"""

__author__ = 'Andrei Savu <contact@andreisavu.ro>'

from SimpleXMLRPCServer import SimpleXMLRPCServer
import settings, generator
import sys,os,xmpp,time

def send_id(channel, params):
    """
    Generate a random ID and send it on the channel 

    Parameters:
        channel - communication channel
        params  - channel configs

    Returns:
        False if it fails
        Random string sent to user on success

    """
    id = generator.id(channel)
    msg = "OTP: %s" % id
    if not send(channel, msg, params):
        return False
    return id

def send(channel, msg, params):
    """
    Send a message on the requested channel

    Parameters:
        channel - communication channel
        msg     - text message
        params  - channel configs

    Returns:
        True or False
    """
    if channel == 'smtp':
        return send_smtp(msg, params)
    elif channel == 'im':
        return send_im(msg, params)
    elif channel == 'sms':
        return send_sms(msg, params)
    return False

def send_smtp(msg, params):
    """
    Send a message using smtp

    Parameters:
        msg     - text message
        params  - to: destination address
    
    Returns:
        True
    """
    import mail
    mail.send(serverURL=settings.SMTP['server'], 
        sender=settings.SMTP['sender'],
        to=params['to'],
        subject=settings.SMTP['subject'],
        text=msg)
    return True

def send_im(msg, params):
    """
    Send a message using jabber/xmpp

    Parameters:
        msg     - text message
        params  - to: some-user@some-jabber-enabled-server

    Returns:
        True or False
    """
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

def send_sms(msg, params):
    """
    Send a message using a phone modem

    Parameters:
        msg     - text message
        params  - to: destination phone number

    Returns:
        True or False

    """
    from subprocess import Popen
    command = ['/usr/bin/gsmsendsms', '-d', settings.SMS['dev'], params['to'], msg]
    p = Popen(command)
    code = p.wait()
    if code != 0:
        return False
    return True

def get_channels():
    """
    Get a list of all available channels with some extra
    data needed for form construction and display
    """
    return [{
        'id':'smtp',
        'name':'Email',
        'description':'Use an email address for receiving the password',
        'params':{'to':'Adress'}
        },{
        'id':'im',
        'name':'Jabber/XMPP',
        'description':'Use a jabber/IM account',
        'params':{'to':'Account'}
        },{
        'id':'sms',
        'name':'Phone SMS',
        'description':'Use mobile phone',
        'params':{'to':'Phone'}
        }]

def main(argv):
    """
    Main function

    Start an xml-rpc server on a given port (by default 8000)
    and listen for message send requests.
    """
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

