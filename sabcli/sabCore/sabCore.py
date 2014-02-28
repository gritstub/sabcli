import sys

class sabCore():
    def __init__(self):
        self.channel = sys.modules["__main__"].channel
        self.encoder = sys.modules["__main__"].encoder
        self.parser = sys.modules["__main__"].parser

    def sendCommand(self, command):
        path = self.encoder.encodeQuery(command)
        # TODO: figure out the other variables
        self.channel.sendCommand(path, {}, {})

    def list(self, command):
        result = {}
        path = self.encoder.encodeQuery(command)
        response = self.channel.requestData(path)
        if response:
            result = self.parser.parse(response)
        return result