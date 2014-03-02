import sys

class sabCore():
    def __init__(self):
        self.channel = sys.modules["__main__"].channel
        self.encoder = sys.modules["__main__"].encoder
        self.parser = sys.modules["__main__"].parser

    def sendHistoryCommand(self, command, args):
        path = self.encoder.encodeHistoryCommand(command, args)
        self.channel.sendCommand(path)

    def sendQueueCommand(self, command, args):
        path = self.encoder.encodeQueueCommand(command, args)
        self.channel.sendCommand(path)

    def list(self, command):
        result = {}
        path = self.encoder.encodeQuery(command)
        response = self.channel.requestData(path)
        if response:
            result = self.parser.parse(response)
        return result