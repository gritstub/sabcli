import nose
from mock import Mock, PropertyMock, patch
import BaseTestCase
from sabCore import sabChannel


class sabChannel_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        self.config = Mock()
        type(self.config).username = PropertyMock(return_value = "")
        type(self.config).password = PropertyMock(return_value = "")

        self.test_channel = sabChannel.sabChannel(settings=self.config)

    def test_should_instantiate(self):
        assert(isinstance(self.test_channel, sabChannel.sabChannel))

    def test_requestData_should_call_send(self):
        self.test_channel._send = Mock()

        self.test_channel.requestData("path")

        self.test_channel._send.assert_called_with("path")

    def test_sendCommand_should_call_send(self):
        self.test_channel._send = Mock()

        self.test_channel.sendCommand("path")

        self.test_channel._send.assert_called_with("path")

    @patch('sabCore.sabChannel.urllib2.Request')
    @patch('sabCore.sabChannel.urllib2.urlopen')
    def test_send_should_use_urllib2_request_correctly(self, mock_request, mock_urlopen):

        self.test_channel._send("path")

        assert(mock_request.called is True)

    @patch('sabCore.sabChannel.urllib2.urlopen')
    def test_send_should_use_urllib2_correctly(self, mock_urlopen):
        mock_read = Mock()
        mock_read.read.side_effect = ["test"]
        mock_urlopen.return_value = mock_read

        value = self.test_channel._send("path")

        assert(value == "test")
        assert(mock_urlopen.called is True)
        assert(mock_read.read.called is True)

if __name__ == '__main__':
    nose.runmodule()