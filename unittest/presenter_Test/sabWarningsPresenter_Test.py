import nose
import BaseTestCase
from mock import Mock
from cursesUI import cursesWindow
from presenters.sabWarningsPresenter import sabWarningsPresenter


class sabWarningsPresenter_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.test_presenter = sabWarningsPresenter(window=Mock(spec=cursesWindow.cursesWindow))

    def test_should_instantiate(self):
        assert(isinstance(self.test_presenter, sabWarningsPresenter))

    def test_display_should_call_displayGeneralInformation(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayScrollAndItemSelection = Mock()
        self.test_presenter.displayWarnings = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayGeneralInformation.assert_called_with()

    def test_display_should_call_displayWarnings(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayScrollAndItemSelection = Mock()
        self.test_presenter.displayWarnings = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayWarnings.assert_called_with({})

    def test_display_should_draw_window_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayScrollAndItemSelection = Mock()
        self.test_presenter.displayWarnings = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.draw.assert_called_with([])

    def test_display_should_draw_pad_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayScrollAndItemSelection = Mock()
        self.test_presenter.displayWarnings = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.pad.draw.assert_called_with([])

    def test_display_should_call_displayScrollAndItemSelection(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayScrollAndItemSelection = Mock()
        self.test_presenter.displayWarnings = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.pad.draw.assert_called_with([])

    def test_displayGeneralInformation_should_update_screen_with_instructions(self):
        self.test_presenter.window.size = ["50", "50"]

        self.test_presenter.displayGeneralInformation()

        assert len(self.test_presenter.screen) == 2

    def test_displayWarning_should_call_displayWarningInformation(self):
        self.test_presenter.displayWarningInformation = Mock()

        self.test_presenter.displayWarnings({"warnings": [{}]})

        self.test_presenter.displayWarningInformation.assert_called_with({"item_length": 1})

    def test_displayWarningInformation_should_add_pad_instructions(self):
        self.test_presenter.window.size = ["50", "50"]
        self.test_presenter.fitWarningMessageToWindow = Mock()
        self.test_presenter.displayWarningMessage = Mock()

        self.test_presenter.displayWarningInformation({"timestamp": "00:00:00", "type": "test_type", "message": "test_message"})

        assert len(self.test_presenter.pad) == 4

    def test_displayWarningInformation_should_call_fitWarningMessageToWindow(self):
        self.test_presenter.window.size = ["50", "50"]
        self.test_presenter.fitWarningMessageToWindow = Mock()
        self.test_presenter.displayWarningMessage = Mock()

        self.test_presenter.displayWarningInformation({"timestamp": "00:00:00", "type": "test_type", "message": "test_message"})

        self.test_presenter.fitWarningMessageToWindow.assert_called_with({"timestamp": "00:00:00", "type": "test_type", "message": "test_message"})

    def test_displayWarningInformation_should_call_displayWarningMessage(self):
        self.test_presenter.window.size = ["50", "50"]
        self.test_presenter.fitWarningMessageToWindow = Mock()
        self.test_presenter.displayWarningMessage = Mock()

        self.test_presenter.displayWarningInformation({"timestamp": "00:00:00", "type": "test_type", "message": "test_message"})

        self.test_presenter.displayWarningMessage.assert_called_with({"timestamp": "00:00:00", "type": "test_type", "message": "test_message"})

    def test_fitWarningMessageToWindow_should_populate_item_length(self):
        self.test_presenter.window.size = ["50", "45"]

        warning = {"timestamp": "00:00:00", "type": "test_type", "message": "test1 test2 test3"}
        self.test_presenter.fitWarningMessageToWindow(warning)

        assert "item_length" in warning

    def test_fitWarningMessageToWindow_should_populate_lines(self):
        self.test_presenter.window.size = ["50", "45"]

        warning = {"timestamp": "00:00:00", "type": "test_type", "message": "test1 test2 test3"}
        self.test_presenter.fitWarningMessageToWindow(warning)

        assert "lines" in warning

    def test_displayWarningMessage_should_add_pad_instructions(self):
        self.test_presenter.window.size = ["50", "45"]

        self.test_presenter.displayWarningMessage({"lines": ["line 1", "line 2", "line 3"]})

        assert len(self.test_presenter.pad) == 6

if __name__ == '__main__':
    nose.runmodule()