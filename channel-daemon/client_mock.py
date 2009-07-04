
class Client:

    def __init__(self, url):
        self.url = url

    def send(self, channel, msg, params):
        print "Send: %s, %s" % (channel, msg)
        return True

    def send_id(self, channel, params):
        print "SendID: %s" % channel
        return "12345"

    def get_channels(self):
        return [{
            'id':'smtp',
            'name':'Email',
            'description':'Use an email address for receiving the password',
            'params':{'to':'Adresa'}
            }]


