import nose
import BaseTestCase
from mock import Mock
from cursesUI import cursesWindow
from presenters.sabStatusPresenter import sabStatusPresenter


class sabStatusPresenter_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.test_presenter = sabStatusPresenter(window=Mock(spec=cursesWindow.cursesWindow))

    def test_should_instantiate(self):
        assert(isinstance(self.test_presenter, sabStatusPresenter))

    def test_display_should_call_displayDiskWarning(self):
        self.test_presenter.displayDiskWarning = Mock()
        self.test_presenter.displayGeneralStatus = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayDiskWarning.assert_called_with({})

    def test_display_should_call_displayGeneralStatus(self):
        self.test_presenter.displayDiskWarning = Mock()
        self.test_presenter.displayGeneralStatus = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayGeneralStatus.assert_called_with({})

    def test_display_should_draw_window_instructions(self):
        self.test_presenter.displayDiskWarning = Mock()
        self.test_presenter.displayGeneralStatus = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.draw.assert_called_with([])

    def test_display_should_draw_pad_instructions(self):
        self.test_presenter.displayDiskWarning = Mock()
        self.test_presenter.displayGeneralStatus = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.pad.draw.assert_called_with([])

    def test_displayDiskWarning_should_not_add_screen_instructions_if_there_are_no_warnings(self):

        self.test_presenter.displayDiskWarning({})

        assert len(self.test_presenter.screen) == 0

    def test_displayDiskWarning_should_add_screen_instructions_if_there_are_warnings(self):

        self.test_presenter.displayDiskWarning({"warning": "world_exploding"})

        assert len(self.test_presenter.screen) == 1

    def test_displayGeneralStatus_should_add_screen_instructions(self):
        self.test_presenter.printLine = Mock()
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displayGeneralStatus({"disk_usage": "test", "main_stats": "test", "last_update": "test"})

        assert len(self.test_presenter.screen) == 1

    def test_displayGeneralStatus_should_call_print_line_to_build_status_line(self):
        self.test_presenter.printLine = Mock()
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displayGeneralStatus({"disk_usage": "test1", "main_stats": "test2", "last_update": "test3"})

        self.test_presenter.printLine.assert_was_called("test1", "test2", "test3")

    def test_printLine_should(self):
        self.test_presenter.window.size = ["20", "20"]

        result = self.test_presenter.printLine(["test1", "test2", "test3"])

        assert(result == "test1  test2  test3")

    def test_displayFetching_should_add_screen_instruction(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayFetching()

        assert len(self.test_presenter.screen) == 1

    def test_displayFetching_should_draw_screen(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayFetching()

        assert self.test_presenter.window.draw.called

    def test_displayFetching_should_refresh_window(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.window.pad = Mock()

        self.test_presenter.displayFetching()

        assert self.test_presenter.window.refresh.called

if __name__ == '__main__':
    nose.runmodule()