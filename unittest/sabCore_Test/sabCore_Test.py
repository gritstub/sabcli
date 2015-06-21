import nose
import BaseTestCase
from mock import Mock
from sabCore import core


class sabCore_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.encoder = Mock(spec=core.sabEncoder)
        self.channel = Mock(spec=core.sabChannel)
        self.parser = Mock(spec=core.sabParser)
        self.test_core = core.core(channel=self.channel, encoder=self.encoder, parser=self.parser)

    def test_should_instantiate(self):
        assert(isinstance(self.test_core, core.core))

    def test_sendGeneralCommand_should_encode_command(self):
        self.test_core.sendGeneralCommand("command")

        self.encoder.encodeGeneralCommand.assert_called_with("command")

    def test_sendGeneralCommand_should_send_through_channel(self):
        self.encoder.encodeGeneralCommand.return_value = "path"

        self.test_core.sendGeneralCommand("")

        self.channel.sendCommand.assert_called_with("path")

    def test_sendHistoryCommand_should_encode_command(self):
        self.test_core.sendHistoryCommand("command", "id")

        self.encoder.encodeHistoryCommand.assert_called_with("command", ("id",))

    def test_sendHistoryCommand_should_send_through_channel(self):
        self.encoder.encodeHistoryCommand.return_value = "path"

        self.test_core.sendHistoryCommand("", "")

        self.channel.sendCommand.assert_called_with("path")

    def test_sendQueueCommand_should_encode_command(self):
        self.test_core.sendQueueCommand("command", "id")

        self.encoder.encodeQueueCommand.assert_called_with("command", ("id",))

    def test_sendQueueCommand_should_send_through_channel(self):
        self.encoder.encodeQueueCommand.return_value = "path"

        self.test_core.sendQueueCommand("", "")

        self.channel.sendCommand.assert_called_with("path")

    def test_list_should_encode_query(self):

        self.test_core.list("listing")

        self.encoder.encodeQuery.assert_called_with("listing")

    def test_list_should_request_data(self):
        self.encoder.encodeQuery.return_value = "path"

        self.test_core.list("")

        self.channel.requestData.assert_called_with("path")

    def test_list_should_parse_valid_responses(self):
        self.encoder.encodeQuery.return_value = "path"
        self.channel.requestData.return_value = "data"

        self.test_core.list("")

        self.parser.parse.assert_called_with("data")

    def test_list_should_not_parse_empty_responses(self):
        self.encoder.encodeQuery.return_value = "path"
        self.channel.requestData.return_value = ""

        self.test_core.list("")

        assert(self.parser.parse.called is False)

if __name__ == '__main__':
    nose.runmodule()