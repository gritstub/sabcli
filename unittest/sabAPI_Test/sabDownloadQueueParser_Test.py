from mock import Mock, patch
import nose
import BaseTestCase
from sabAPI import sabDownloadQueueParser


class sabDownloadQueueParser_Test(BaseTestCase.BaseTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()

        self.test_parser = sabDownloadQueueParser.sabQueueParser()

    def test_should_instantiate(self):
        assert (isinstance(self.test_parser, sabDownloadQueueParser.sabQueueParser))

    @patch('sabAPI.sabQueueParser.time.time')
    def test_parse_should_extract_general_queue_state(self, mock_time):
        mock_time.return_value = "000001"
        self.test_parser.parseQueue = Mock(return_value="queue")
        response = {"queue": {"status": "queue_status_test",
                        "kbpersec": "90", "sizeleft": "100",
                        "timeleft": "test_time", "mb": "1000",
                        "mbleft": "100", "diskspace2": "2000",
                        "diskspacetotal2": "20000", "uptime": "2300"}}

        result = self.test_parser.parse(response)

        assert (result == {'status': 'queue_status_test',
                           'time_left': 'test_time',
                           'downloaded': 0.87890625,
                           'mbleft': '100',
                           'diskspace2': '2000',
                           'speed': '90.00 kb/s',
                           'uptime': '2300',
                           'progress_pct': 89.99910000899992,
                           'mb': '1000',
                           'total_queue': 0.9765625,
                           'last_fetch_time': '000001',
                           'size_left': '100',
                           'diskspacetotal2': '20000',
                           'queue': 'queue'})

    def test_parseQueue_should_extract_queue_details(self):
        response = {"queue": {"slots": [{"id": 1, "filename": "test_name", "index": 0, "unpackopts": "1",
                                         "avg_age": "3 Weeks", "size": "100", "nzo_id": "nzo_1", "mb": "100",
                                         "status": "fine", "priority": "high", "timeleft": '000001',
                                         "mbleft": "10", "percentage": "90"}]}}

        result = self.test_parser.parseQueue(response)

        assert (result == [{'filename': 'test_name', 'index': 0, "avg_age": "3 Weeks", "priority": "high",
                            "unpackopts": 1, "mb": "100", "percentage": "90", "mb_left": "10", "timeleft": '000001',
                            'id': 'nzo_1', 'status': 'fine'}])

if __name__ == '__main__':
    nose.runmodule()