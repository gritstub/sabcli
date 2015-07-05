import nose
from mock import Mock, PropertyMock, patch
import BaseTestCase
from sabCore import sabEncoder


class sabEncoder_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        self.config = Mock()
        type(self.config).host = PropertyMock(return_value = "localhost")
        type(self.config).port = PropertyMock(return_value = "8080")
        type(self.config).apikey = PropertyMock(return_value = "1234")

        self.test_encoder = sabEncoder.sabEncoder(settings=self.config)

    def test_should_instantiate(self):
        assert(isinstance(self.test_encoder, sabEncoder.sabEncoder))

    def test_encodeQuery_should_construct_version_url_correctly(self):

        url = self.test_encoder.encodeQuery("version")

        assert(url == "http://localhost:8080/api?apikey=1234&mode=version&output=json")

    def test_encodeQuery_should_construct_warning_url_correctly(self):

        url = self.test_encoder.encodeQuery("warning")

        assert(url == "http://localhost:8080/api?apikey=1234&mode=warning&output=json")

    def test_encodeQuery_should_construct_queue_url_correctly(self):

        url = self.test_encoder.encodeQuery("queue")

        assert(url == "http://localhost:8080/api?apikey=1234&mode=queue&start=START&limit=LIMIT&output=json")

    def test_encodeQuery_should_construct_history_url_correctly(self):

        url = self.test_encoder.encodeQuery("history")

        assert(url == "http://localhost:8080/api?apikey=1234&mode=history&start=START&limit=LIMIT&output=json")

    def test_encodeQuery_should_construct_details_action_urls_correctly(self):

        url = self.test_encoder.encodeQuery("details", "1")

        assert(url == "http://localhost:8080/api?apikey=1234&mode=get_files&value=1&output=json")


    def test_encodeGeneralCommand_should_contstruct_generic_command_urls_correctly(self):

        url = self.test_encoder.encodeGeneralCommand("command")

        assert(url == "http://localhost:8080/api?apikey=1234&mode=command&output=json")

    def test_encodeQueueCommand_should_construct_change_complete_action_urls_correctly(self):

        url = self.test_encoder.encodeQueueCommand("queuecompleted", ["unpack"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=queue&name=change_complete_action&value=unpack")

    def test_encodeQueueCommand_should_construct_delete_action_urls_correctly(self):

        url = self.test_encoder.encodeQueueCommand("delete", ["1"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=queue&name=delete&value=1")

    def test_encodeQueueCommand_should_construct_pause_action_urls_correctly(self):

        url = self.test_encoder.encodeQueueCommand("pause", ["1"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=queue&name=pause&value=1")

    def test_encodeQueueCommand_should_construct_resume_action_urls_correctly(self):

        url = self.test_encoder.encodeQueueCommand("resume", ["1"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=queue&name=resume&value=1")

    def test_encodeQueueCommand_should_construct_rename_action_urls_correctly(self):

        url = self.test_encoder.encodeQueueCommand("rename", ["1", "test_name"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=queue&name=rename&value=1&value2=test_name")

    def test_encodeQueueCommand_should_construct_priority_action_urls_correctly(self):

        url = self.test_encoder.encodeQueueCommand("priority", ["1", "high"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=queue&name=priority&value=1&value2=high")

    def test_encodeQueueCommand_should_construct_postprocessing_action_urls_correctly(self):

        url = self.test_encoder.encodeQueueCommand("postprocessing", ["1", "par2"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=change_opts&value=1&value2=par2")

    def test_encodeQueueCommand_should_construct_move_action_urls_correctly(self):

        url = self.test_encoder.encodeQueueCommand("move", ["1", "2"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=switch&value=1&value2=2")

    def test_encodeHistoryCommand_should_clear_history_command_url_correctly(self):

        url = self.test_encoder.encodeHistoryCommand("history", ["clear"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=history&name=delete&value=all")

    def test_encodeHistoryCommand_should_delete_entry_command_url_correctly(self):

        url = self.test_encoder.encodeHistoryCommand("history", ["SABnzbd_nzo_1"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=history&name=delete&value=SABnzbd_nzo_1")

    def test_encodeMiscAction_should_construct_addfile_url_correctly(self):

        url = self.test_encoder.encodeMiscAction("addlocalfile", ["path"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=addlocalfile&name=path")

    def test_encodeMiscAction_should_construct_addurl_url_correctly(self):

        url = self.test_encoder.encodeMiscAction("addurl", ["url"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=addurl&name=url")

    def test_encodeMiscAction_should_construct_addid_url_correctly(self):

        url = self.test_encoder.encodeMiscAction("addid", ["id"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=addid&name=id")

    def test_encodeMiscAction_should_construct_newapikey_url_correctly(self):

        url = self.test_encoder.encodeMiscAction("newapikey", ["confirm"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=config&name=set_apikey")

    def test_encodeMiscAction_should_construct_pause_url_correctly(self):

        url = self.test_encoder.encodeMiscAction("temppause", ["1"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=config&name=set_pause&value=1")

    def test_encodeMiscAction_should_construct_speed_limit_url_correctly(self):

        url = self.test_encoder.encodeMiscAction("speedlimit", ["100"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=config&name=speedlimit&value=100")

    def test_encodeMiscAction_should_construct_auto_shutdown_url_correctly(self):

        url = self.test_encoder.encodeMiscAction("autoshutdown", ["1"])

        assert(url == "http://localhost:8080/api?apikey=1234&mode=autoshutdown&name=1")

if __name__ == '__main__':
    nose.runmodule()