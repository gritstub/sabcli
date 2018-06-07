from mock import Mock, patch
import json
import nose
import BaseTestCase
from sabAPI import sabHistoryParser


class sabHistoryParser_Test(BaseTestCase.BaseTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()

        self.test_parser = sabHistoryParser.sabHistoryParser()

    def test_should_instantiate(self):
        assert (isinstance(self.test_parser, sabHistoryParser.sabHistoryParser))

    @patch('sabAPI.sabHistoryParser.time.time')
    def test_parse_should_extract_main_structure(self, mock_time):
        mock_time.return_value = "000001"
        with open('data/history.json') as f:
            response = json.load(f)

        result = self.test_parser.parse(response)

        assert (result["total_size"] == "678.1 G")
        assert (result["month_size"] == "167.3 G")
        assert (result["week_size"] == "30.4 G")
        assert (result["history"][0]["index"] == 233)
        assert (result["history"][0]["name"] == "TV.Show.S04E13.720p.BluRay.x264-xHD")
        assert (result["history"][0]["size"] == "2.3 GB")
        assert (result["history"][0]["id"] == "SABnzbd_nzo_gqhp63")
        assert (result["history"][0]["status"] == "Completed")
        assert (result["history"][1]["index"] == 234)
        assert (result["history"][1]["name"] == "TV.Show.S04E02.720p.BluRay.x264-xHD")
        assert (result["history"][1]["size"] == "2.3 GB")
        assert (result["history"][1]["id"] == "SABnzbd_nzo_sdkoun")
        assert (result["history"][1]["status"] == "Completed")

    def test_parseHistory_should_extract_history_details(self):
        self.test_parser.extractStageLog = Mock(return_value=[])

        response = {"history": {"slots": [{"id": 1, "name": "test", "size": "100", "nzo_id": "nzo_1", "status": "fine"}]}}

        result = self.test_parser.parseHistory(response)

        assert (result == [{'id': 'nzo_1', 'index': 0, 'status': 'fine', 'name': 'test', 'size': '100'}])

    def test_parseHistory_should_try_to_extract_stage_log(self):
        self.test_parser.extractStageLog = Mock(return_value=[])

        response = {"history": {"slots": [{"id": 1, "name": "test", "size": "100", "nzo_id": "nzo_1", "status": "fine"}]}}

        result = self.test_parser.parseHistory(response)

        self.test_parser.extractStageLog.assert_called_with(response["history"]["slots"][0])

    def test_parseHistory_should_try_to_extract_unpack_details_log(self):
        self.test_parser.extractUnpackOperationStatus = Mock()
        self.test_parser.extractStageLog = Mock(return_value=[{"name": "Unpack"}])

        response = {"history": {"slots": [{"id": 1, "name": "test", "size": "100", "nzo_id": "nzo_1", "status": "fine"}]}}

        result = self.test_parser.parseHistory(response)

        assert (self.test_parser.extractUnpackOperationStatus.called)

    def test_parseHistory_should_try_to_extract_repair_details_log(self):
        self.test_parser.extractRepairOperationStatus = Mock()
        self.test_parser.extractStageLog = Mock(return_value=[{"name": "Repair"}])

        response = {"history": {"slots": [{"id": 1, "name": "test", "size": "100", "nzo_id": "nzo_1", "status": "fine"}]}}

        result = self.test_parser.parseHistory(response)

        assert (self.test_parser.extractRepairOperationStatus.called)

    def test_extractStageLog_should_extract_actions_from_log(self):
        slot = {"stage_log": [{"name": "repair"}]}

        result = self.test_parser.extractStageLog(slot)

        assert (result == slot["stage_log"])

    def test_extractUnpackOperationStatus_should_give_success_on_empty_log(self):
        action = {"actions": []}
        item = {}

        self.test_parser.extractUnpackOperationStatus(action, item)

        assert (item == {"unpack_fail": 0, "unpack_log": []})

    def test_extractUnpackOperationStatus_should_give_failure_on_non_unpacked_entries(self):
        action = {"actions": ["failed"]}
        item = {}

        self.test_parser.extractUnpackOperationStatus(action, item)

        assert (item == {"unpack_fail": 1, "unpack_log": ["failed"]})

    def test_extractUnpackOperationStatus_should_give_success_if_all_entires_are_unpacked(self):
        action = {"actions": ["test Unpacked"]}
        item = {}

        self.test_parser.extractUnpackOperationStatus(action, item)

        assert (item == {"unpack_fail": 0, "unpack_log": []})

    def test_extractRepairOperationStatus_should_give_success_on_empty_log(self):
        action = {"actions": []}
        item = {}

        self.test_parser.extractRepairOperationStatus(action, item)

        assert (item == {"repair_status": 0, "repair_log": []})

    def test_extractRepairOperationStatus_should_give_failure_on_nonrepaired_entries(self):
        action = {"actions": ["failed"]}
        item = {}

        self.test_parser.extractRepairOperationStatus(action, item)

        assert (item == {"repair_status": 2, "repair_log": ["failed"]})

    def test_extractRepairOperationStatus_should_give_success_if_all_entries_are_repaired(self):
        action = {"actions": ["Quick Check OK", "Repaired in", "all files correct"]}
        item = {}

        self.test_parser.extractRepairOperationStatus(action, item)

        assert (item == {"repair_status": 0, "repair_log": []})

if __name__ == '__main__':
    nose.runmodule()