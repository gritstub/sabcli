import nose
import BaseTestCase
from mock import Mock
from sabCore import core
from sabAPI import api
from sabAPI import sabHistoryParser
from sabAPI import sabInfoParser
from sabAPI import sabDownloadQueueParser
from sabAPI import sabWarningsParser


class api_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.core = Mock(spec=core.core)
        self.history_parser = Mock(spec=sabHistoryParser.sabHistoryParser)
        self.info_parser = Mock(spec=sabInfoParser.sabInfoParser)
        self.queue_parser = Mock(spec=sabDownloadQueueParser.sabDownloadQueueParser)
        self.warnings_parser = Mock(spec=sabWarningsParser.sabWarningsParser)

        self.test_api = api.api(sabCore=self.core, queueParser=self.queue_parser, infoParser=self.info_parser,
                                historyParser=self.history_parser, warningsParser=self.warnings_parser)

    def test_should_instantiate(self):
        assert(isinstance(self.test_api, api.api))

    def test_listQueue_should_call_core_list_command(self):
        self.test_api.listQueue()

        self.core.list.assert_called_with("queue")

    def test_listQueue_should_call_correct_parser_with_list_content(self):
        self.core.list.return_value = "list"

        self.test_api.listQueue()

        self.queue_parser.parse.assert_called_with("list")

    def test_listWarnings_should_call_core_list_command(self):
        self.test_api.listWarnings()

        self.core.list.assert_called_with("warnings")

    def test_listWarnings_should_call_correct_parser_with_list_content(self):
        self.core.list.return_value = "warnings"

        self.test_api.listWarnings()

        self.warnings_parser.parse.assert_called_with("warnings")

    def test_listHistory_should_call_core_list_command(self):
        self.test_api.listHistory()

        self.core.list.assert_called_with("history")

    def test_listHistory_should_call_correct_parser_with_list_content(self):
        self.core.list.return_value = "history"

        self.test_api.listHistory()

        self.history_parser.parse.assert_called_with("history")

    def test_getApiInfo_should_call_core_list_command(self):
        self.test_api.getApiInfo()

        self.core.list.assert_called_with("fullstatus")

    def test_getApiInfo_should_call_correct_parser_with_content(self):
        self.core.list.return_value = "info"

        self.test_api.getApiInfo()

        self.info_parser.parse.assert_called_with("info")

    def test_deleteDownload_should_call_core_correctly(self):

        self.test_api.deleteDownload(1)

        self.core.sendQueueCommand.assert_called_with("delete", 1)

    def test_pauseDownload_should_call_core_correctly(self):

        self.test_api.pauseDownload(1)

        self.core.sendQueueCommand.assert_called_with("pause", 1)

    def test_resumeDownload_should_call_core_correctly(self):

        self.test_api.resumeDownload(1)

        self.core.sendQueueCommand.assert_called_with("resume", 1)

    def test_getDownloadFiles_should_call_core_correctly(self):

        self.test_api.listDownloadFiles(1)

        self.core.list.assert_called_with("details", 1)

    def test_renameDownload_should_call_core_correctly(self):

        self.test_api.renameDownload(1, "test")

        self.core.sendQueueCommand.assert_called_with("rename", 1, "test")

    def test_changeDownloadPriority_should_call_core_correctly(self):

        self.test_api.changeDownloadPriority(1, "high")

        self.core.sendQueueCommand.assert_called_with("priority", 1, "high")

    def test_changeDownloadProcessingSteps_should_call_core_correctly(self):

        self.test_api.changeDownloadProcessingSteps(1, "unpack")

        self.core.sendQueueCommand.assert_called_with("postprocessing", 1, "unpack")

    def test_deleteFromHistory_should_call_core_correctly(self):

        self.test_api.deleteFromHistory(1)

        self.core.sendHistoryCommand.assert_called_with("delete", 1)

    def test_clearHistory_should_call_core_correctly(self):

        self.test_api.clearHistory()

        self.core.sendHistoryCommand.assert_called_with("clear")

    def test_pauseServer_should_call_core_correctly(self):

        self.test_api.pauseServer()

        self.core.sendGeneralCommand.assert_called_with("pause")

    def test_resumeServer_should_call_core_correctly(self):

        self.test_api.resumeServer()

        self.core.sendGeneralCommand.assert_called_with("resume")

    def test_shutdownServer_should_call_core_correctly(self):

        self.test_api.shutdownServer()

        self.core.sendGeneralCommand.assert_called_with("shutdown")

if __name__ == '__main__':
    nose.runmodule()