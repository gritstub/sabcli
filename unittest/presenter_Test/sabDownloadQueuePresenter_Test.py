import nose
import BaseTestCase
from mock import Mock
from cursesUI.cursesWindow import cursesWindow
from presenters.sabDownloadQueuePresenter import sabDownloadQueuePresenter
from presenters.sabScrollPresenter import sabScrollPresenter


class sabQueuePresenter_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.test_presenter = sabDownloadQueuePresenter(window=Mock(spec=cursesWindow), scrollPresenter=Mock(spec=sabScrollPresenter))

    def test_should_instantiate(self):
        assert(isinstance(self.test_presenter, sabDownloadQueuePresenter))

    def test_display_should_call_displayGeneralInformation(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayQueue = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayGeneralInformation.assert_called_with()

    def test_display_should_call_displayQueue(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayQueue = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayQueue.assert_called_with({"item_size": 3})

    def test_display_should_draw_window_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayQueue = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.draw.assert_called_with([])

    def test_display_should_call_scrollpresenter_display(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayQueue = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.scrollPresenter.display.assert_called_with({"item_size": 3})

    def test_display_should_draw_pad_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayQueue = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.pad.draw.assert_called_with([])

    def test_display_should_draw_pad_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayQueue = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.pad.draw.assert_called_with([])


    def test_displayGeneralInformation_should_add_screen_instructions_if_views_are_present(self):
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displayGeneralInformation()

        assert len(self.test_presenter.screen) == 2

    def test_displayQueue_should_call_calculateProgressBarPadding(self):
        self.test_presenter.calculateProgressBarPadding = Mock()
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displayQueue({"queue": []})

        self.test_presenter.calculateProgressBarPadding.assert_called_with({"queue": []})

    def test_displayQueue_should_call_displayFileInformation(self):
        self.test_presenter.calculateProgressBarPadding = Mock()
        self.test_presenter.displayFileInformation = Mock()
        self.test_presenter.displayProgress = Mock()
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displayQueue({"current_index": 1, "current_selection": 1, "queue": [{"index": 0}]})

        self.test_presenter.displayFileInformation.assert_called_with({"index": 0})

    def test_displayQueue_should_call_displayFileInformation_with_selection_information_for_selected_item(self):
        self.test_presenter.calculateProgressBarPadding = Mock()
        self.test_presenter.displayFileInformation = Mock()
        self.test_presenter.displayProgress = Mock()
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displayQueue({"current_index": 0, "current_selection": 1, "queue": [{"index": 0}]})

        self.test_presenter.displayFileInformation.assert_called_with({"index": 0}, 1)

    def test_displayQueue_should_call_displayProgress(self):
        self.test_presenter.calculateProgressBarPadding = Mock(return_value="padding")
        self.test_presenter.displayFileInformation = Mock()
        self.test_presenter.displayProgress = Mock()
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displayQueue({"current_index": 1, "current_selection": 1, "queue": [{"index": 0}]})

        self.test_presenter.displayProgress.assert_called_with("padding", {"index": 0})

    def test_calculateProgressBarPadding(self):

        result = self.test_presenter.calculateProgressBarPadding({"queue": [{"mb": "1000"}]})

        assert result == 8

    def test_displayFileInformation_should_add_pad_instructions(self):

        self.test_presenter.displayFileInformation({"index": 0, "filename": "test_name", "avg_age": "3 Days",
                                                    "priority": "high", "unpackopts": "1", "status": "paused"})
        assert len(self.test_presenter.pad) == 13
        assert len(self.test_presenter.screen) == 0

    def test_displayFileInformation_should_highlight_filename(self):

        self.test_presenter.displayFileInformation({"index": 0, "filename": "test_name", "avg_age": "3 Days",
                                                    "priority": "high", "unpackopts": "1", "status": "paused"}, 0)

        assert self.test_presenter.pad[3][1] == 2

    def test_displayFileInformation_should_highlight_priority(self):

        self.test_presenter.displayFileInformation({"index": 0, "filename": "test_name", "avg_age": "3 Days",
                                                    "priority": "high", "unpackopts": "1", "status": "paused"}, 1)

        assert self.test_presenter.pad[7][1] == 2

    def test_displayFileInformation_should_highlight_unpack_settings(self):

        self.test_presenter.displayFileInformation({"index": 0, "filename": "test_name", "avg_age": "3 Days",
                                                    "priority": "high", "unpackopts": "1", "status": "paused"}, 2)

        assert self.test_presenter.pad[9][1] == 2

    def test_displayProgress_should_add_pad_instructions(self):
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displayProgress(10, {"timeleft": "00:00:01", "mb": "100", "mb_left": "10", "percentage": "90"})

        assert len(self.test_presenter.pad) == 11
        assert len(self.test_presenter.screen) == 0

    def test_editDownloadName_should_call_scrollPresenter_to_get_view_ports_current_line(self):
        self.test_presenter.scrollPresenter.calculateScrollingLine = Mock(return_value = 1)
        self.test_presenter.window = Mock()
        state = {"item_size": 2, "queue": [{}, {"filename": "test"}]}

        self.test_presenter.editDownloadName(1, state)

        self.test_presenter.scrollPresenter.calculateScrollingLine.assert_called_with(state)

    def test_editDownloadName_should_calculate_current_editing_line_based_on_view_ports_current_line(self):
        self.test_presenter.scrollPresenter.calculateScrollingLine = Mock(return_value = 0)
        self.test_presenter.window = Mock()
        state = {"item_size": 3, "queue": [{}, {"filename": "test"}]}

        self.test_presenter.editDownloadName(1, state)

        line_pad_index = 3 * 1
        line_scroll_index = 0
        edit_line = line_pad_index - line_scroll_index + 4
        self.test_presenter.window.editTextOnScreen.assert_called_with(edit_line, state["queue"][1]["filename"])

if __name__ == '__main__':
    nose.runmodule()