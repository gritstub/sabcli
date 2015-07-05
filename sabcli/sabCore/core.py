from sabCore.sabChannel import sabChannel
from sabCore.sabEncoder import sabEncoder
from sabCore.sabParser import sabParser


class core():
    def __init__(self, channel = None, encoder = None, parser = None):
        if not channel:
            channel = sabChannel()
        self.channel = channel

        if not encoder:
            encoder = sabEncoder()
        self.encoder = encoder

        if not parser:
            parser = sabParser()
        self.parser = parser

    def sendGeneralCommand(self, command):
        path = self.encoder.encodeGeneralCommand(command)
        self.channel.sendCommand(path)

    def sendHistoryCommand(self, command, *args):
        path = self.encoder.encodeHistoryCommand(command, args)
        self.channel.sendCommand(path)

    def sendQueueCommand(self, command, *args):
        path = self.encoder.encodeQueueCommand(command, args)
        self.channel.sendCommand(path)

    def list(self, command, *args):
        result = {}
        path = self.encoder.encodeQuery(command, *args)
        response = self.channel.requestData(path)
        if response:
            result = self.parser.parse(response)
        return result