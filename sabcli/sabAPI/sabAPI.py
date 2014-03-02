import sys

class sabAPI():

    def __init__(self):
        self.core = sys.modules["__main__"].core
        self.infoParser = sys.modules["__main__"].infoParser
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

    def getApiInfo(self):
        info = self.core.list("version")
        return self.infoParser.parse(info)

    def deleteDownload(self, id):
        self.core.sendQueueCommand("delete", id)

    def pauseDownload(self, id):
        self.core.sendQueueCommand("pause", id)

    def resumeDownload(self, id):
        self.core.sendQueueCommand("resume", id)

    def renameDownload(self, id, new_name):
        self.core.sendQueueCommand("rename", id, new_name)

    def changeDownloadPriority(self, id, priority):
        self.core.sendQueueCommand("priority", id, priority)

    def changeDownloadPostProcessing(self, id, steps):
        self.core.sendQueueCommand("postprocessing", id, steps)

    def deleteDownloadHistory(self, id):
        self.core.sendHistoryCommand("delete", id)