"""
Simple client for message gateway server
"""

import xmlrpclib as rpc

class Client:

    def __init__(self, url):
        self.url = url
        self.server = rpc.ServerProxy(url)

    def send(self, channel, msg, params):
        return self.server.send(channel, msg, params)

    def send_id(self, channel, params):
        return self.server.send_id(channel, params)

    def get_channels(self):
        return self.server.get_channels()

