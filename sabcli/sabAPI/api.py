from sabAPI.sabHistoryParser import sabHistoryParser
from sabAPI.sabInfoParser import sabInfoParser
from sabAPI.sabDownloadQueueParser import sabDownloadQueueParser
from sabAPI.sabWarningsParser import sabWarningsParser
from sabCore.core import core


class api():
    def __init__(self, sabCore=None, queueParser=None, infoParser=None, historyParser=None, warningsParser=None):
        if not sabCore:
            sabCore = core()
        self.core = sabCore

        if not queueParser:
            queueParser = sabDownloadQueueParser()
        self.queueParser = queueParser

        if not infoParser:
            infoParser = sabInfoParser()
        self.infoParser = infoParser

        if not historyParser:
            historyParser = sabHistoryParser()
        self.historyParser = historyParser

        if not warningsParser:
            warningsParser = sabWarningsParser()
        self.warningsParser = warningsParser

    # Listings
    def listQueue(self):
        queue = self.core.list("queue")
        return self.queueParser.parse(queue)

    def listWarnings(self):
        warnings = self.core.list("warnings")
        return self.warningsParser.parse(warnings)

    def listHistory(self):
        history = self.core.list("history")
        return self.historyParser.parse(history)

    def listDownloadFiles(self, download_id):
        return self.core.list("details", download_id)

    def getApiInfo(self):
        info = self.core.list("version")
        return self.infoParser.parse(info)

    # Download manipulation
    def deleteDownload(self, download_id):
        self.core.sendQueueCommand("delete", download_id)

    def pauseDownload(self, download_id):
        self.core.sendQueueCommand("pause", download_id)

    def resumeDownload(self, download_id):
        self.core.sendQueueCommand("resume", download_id)

    def renameDownload(self, download_id, new_name):
        self.core.sendQueueCommand("rename", download_id, new_name)

    def changeDownloadPriority(self, download_id, priority):
        self.core.sendQueueCommand("priority", download_id, priority)

    def changeDownloadProcessingSteps(self, download_id, steps):
        self.core.sendQueueCommand("postprocessing", download_id, steps)

    # History Manipulation
    def deleteFromHistory(self, download_id):
        self.core.sendHistoryCommand("delete", download_id)

    def clearHistory(self):
        self.core.sendHistoryCommand("clear")

    # Server Commands
    def pauseServer(self):
        self.core.sendGeneralCommand("pause")

    def resumeServer(self):
        self.core.sendGeneralCommand("resume")

    def shutdownServer(self):
        self.core.sendGeneralCommand("shutdown")

