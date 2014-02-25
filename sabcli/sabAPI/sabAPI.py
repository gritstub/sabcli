import sys

class sabAPI():

    def __init__(self):
        self.core = sys.modules["__main__"].core
        self.queueParser = sys.modules["__main__"].queueParser
        self.historyParser = sys.modules["__main__"].historyParser
        self.warningsParser= sys.modules["__main__"].warningsParser

    def listQueue(self):
        queue = self.core.list("queue")
        return self.queueParser.parse(queue)

    def listWarnings(self):
        warnings = self.core.list("warnings")
        return self.warningsParser.parse(warnings)

    def listHistory(self):
        history = self.core.list("history")
        return self.historyParser.parse(history)

    def getSABStatus(self):
        per = {}