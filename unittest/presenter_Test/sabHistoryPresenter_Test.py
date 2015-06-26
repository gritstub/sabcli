import nose
import BaseTestCase
from mock import Mock
from cursesUI import cursesWindow
from presenters.sabFlexibleScrollPresenter import sabFlexibleScrollPresenter
from presenters.sabHistoryPresenter import sabHistoryPresenter


class sabHistoryPresenter_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.test_presenter = sabHistoryPresenter(window=Mock(spec=cursesWindow.cursesWindow), scrollPresenter=Mock(spec=sabFlexibleScrollPresenter))

    def test_should_instantiate(self):
        assert(isinstance(self.test_presenter, sabHistoryPresenter))

    def test_display_should_call_displayGeneralInformation(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayScrollAndItemSelection = Mock()
        self.test_presenter.displayHistory = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayGeneralInformation.assert_called_with()

    def test_display_should_call_displayHistory(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayScrollAndItemSelection = Mock()
        self.test_presenter.displayHistory = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayHistory.assert_called_with({})

    def test_display_should_draw_window_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayScrollAndItemSelection = Mock()
        self.test_presenter.displayHistory = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.draw.assert_called_with([])

    def test_display_should_draw_pad_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayScrollAndItemSelection = Mock()
        self.test_presenter.displayHistory = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.pad.draw.assert_called_with([])

    def test_display_should_call_displayScrollAndItemSelection(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayScrollAndItemSelection = Mock()
        self.test_presenter.displayHistory = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayScrollAndItemSelection.assert_called_with({})

    def test_displayGeneralInformation_should_add_screen_instructions(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.displayNavigationInformation = Mock()

        self.test_presenter.displayGeneralInformation()

        assert len(self.test_presenter.screen) == 2

    def test_displayHistory_should_update_pad_with_general_information(self):
        self.test_presenter.displayDownloadInformation = Mock()
        self.test_presenter.displayRepairStatus = Mock()
        self.test_presenter.displayUnpackStatus = Mock()
        self.test_presenter.displayRepairLog = Mock()
        self.test_presenter.displayUnpackLog = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayHistory({"history": [{}]})

        assert len(self.test_presenter.pad) == 2

    def test_displayHistory_should_call_displayDownloadInformation(self):
        self.test_presenter.displayDownloadInformation = Mock()
        self.test_presenter.displayRepairStatus = Mock()
        self.test_presenter.displayUnpackStatus = Mock()
        self.test_presenter.displayRepairLog = Mock()
        self.test_presenter.displayUnpackLog = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayHistory({"history": [{}]})

        self.test_presenter.displayDownloadInformation.assert_called_with(0, {"item_length": 2})

    def test_displayHistory_should_call_displayRepairStatus(self):
        self.test_presenter.displayDownloadInformation = Mock()
        self.test_presenter.displayRepairStatus = Mock()
        self.test_presenter.displayUnpackStatus = Mock()
        self.test_presenter.displayRepairLog = Mock()
        self.test_presenter.displayUnpackLog = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayHistory({"history": [{}]})

        self.test_presenter.displayRepairStatus.assert_called_with({"item_length": 2})

    def test_displayHistory_should_call_displayUnpackStatus(self):
        self.test_presenter.displayDownloadInformation = Mock()
        self.test_presenter.displayRepairStatus = Mock()
        self.test_presenter.displayUnpackStatus = Mock()
        self.test_presenter.displayRepairLog = Mock()
        self.test_presenter.displayUnpackLog = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayHistory({"history": [{}]})

        self.test_presenter.displayUnpackStatus.assert_called_with({"item_length": 2})

    def test_displayHistory_should_call_displayRepairLog(self):
        self.test_presenter.displayDownloadInformation = Mock()
        self.test_presenter.displayRepairStatus = Mock()
        self.test_presenter.displayUnpackStatus = Mock()
        self.test_presenter.displayRepairLog = Mock()
        self.test_presenter.displayUnpackLog = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayHistory({"history": [{}]})

        self.test_presenter.displayRepairLog.assert_called_with({"item_length": 2})

    def test_displayHistory_should_call_displayUnpackLog(self):
        self.test_presenter.displayDownloadInformation = Mock()
        self.test_presenter.displayRepairStatus = Mock()
        self.test_presenter.displayUnpackStatus = Mock()
        self.test_presenter.displayRepairLog = Mock()
        self.test_presenter.displayUnpackLog = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayHistory({"history": [{"item_length": 2}]})

        self.test_presenter.displayUnpackLog.assert_called_with({"item_length": 2})

    def test_displayScrollAndItemSelection_should_call_scrollpresenter(self):
        self.test_presenter.scrollPresenter = Mock()

        self.test_presenter.displayScrollAndItemSelection({"history":[{"item_length": 1}], "current_index": 0})

        self.test_presenter.scrollPresenter.display.assert_called_with({"selected_item_start": 0, "current_index": 0,
                                                                        "list_length": 2, "item_lengths": [1],
                                                                        "history": [{"item_length": 1}]})

    def test_displayDownloadInformation_should_update_pad(self):
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayDownloadInformation(0, {"name": "test", "size": "1"})

        assert len(self.test_presenter.pad) == 3

    def test_displayRepairStatus_should_not_update_pad_if_item_doesnt_have_a_repair_status(self):
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayRepairStatus({})

        assert len(self.test_presenter.pad) == 0

    def test_displayRepairStatus_should_display_failure_if_repair_status_is_true(self):
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayRepairStatus({"repair_status": 1})

        assert len(self.test_presenter.pad) == 3
        assert self.test_presenter.pad[1][0] == "FAIL"

    def test_displayRepairStatus_should_display_ok_if_repair_status_is_false(self):
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayRepairStatus({"repair_status": 0})

        assert len(self.test_presenter.pad) == 3
        assert self.test_presenter.pad[1][0] == "OK"

    def test_displayUnpackStatus_should_not_update_pad_if_item_doesnt_have_a_unpack_status(self):
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayUnpackStatus({})

        assert len(self.test_presenter.pad) == 0

    def test_displayUnpackStatus_should_display_failure_if_unpack_status_is_true(self):
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayUnpackStatus({"unpack_status": 1})

        assert len(self.test_presenter.pad) == 3
        assert self.test_presenter.pad[1][0] == "FAIL"

    def test_displayUnpackStatus_should_display_ok_if_unpack_status_is_false(self):
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayUnpackStatus({"unpack_status": 0})

        assert len(self.test_presenter.pad) == 3
        assert self.test_presenter.pad[1][0] == "OK"

    def test_displayRepairLog_should_not_update_pad_if_item_doesnt_have_a_repair_log(self):
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayRepairLog({})

        assert len(self.test_presenter.pad) == 0

    def test_displayRepairLog_should_update_pad_if_item_has_a_standard_repair_log_entry(self):
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayRepairLog({"repair_log": ["smokey.nzb Repair failed 100 blocks missing"]})

        assert len(self.test_presenter.pad) == 2

    def test_displayRepairLog_should_also_update_pad_if_item_has_a_non_standard_repair_log_entry(self):
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayRepairLog({"repair_log": ["some other message"]})

        assert len(self.test_presenter.pad) == 1

    def test_displayRepairLog_should_calculate_item_length(self):
        self.test_presenter.window.pad = Mock()

        result = {"repair_log": ["some other message"]}
        self.test_presenter.displayRepairLog(result)

        assert "item_length" in result

    def test_displayUnpackLog_should_not_update_pad_if_item_doesnt_have_a_unpack_log(self):
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayUnpackLog({})

        assert len(self.test_presenter.pad) == 0

    def test_displayUnpackLog_should_also_update_pad_if_item_has_a_non_standard_unpack_log_entry(self):
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayUnpackLog({"unpack_log": ["some other message"]})

        assert len(self.test_presenter.pad) == 1

    def test_displayUnpackLog_should_calculate_item_length(self):
        self.test_presenter.window.pad = Mock()

        result = {"unpack_log": ["some other message"]}
        self.test_presenter.displayUnpackLog(result)

        assert "item_length" in result


if __name__ == '__main__':
    nose.runmodule()