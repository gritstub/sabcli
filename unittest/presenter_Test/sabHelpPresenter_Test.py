import nose
import BaseTestCase
from mock import Mock
from cursesUI import cursesWindow
from presenters.sabHelpPresenter import sabHelpPresenter


class sabHelpPresenter_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.test_presenter = sabHelpPresenter(window=Mock(spec=cursesWindow.cursesWindow))

    def test_should_instantiate(self):
        assert(isinstance(self.test_presenter, sabHelpPresenter))

    def test_display_should_call_displayGeneralInformation(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayNavigationInformation = Mock()
        self.test_presenter.displayQueueViewInformation = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayGeneralInformation.assert_called_with()

    def test_display_should_call_displayNavigationInformation(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayNavigationInformation = Mock()
        self.test_presenter.displayQueueViewInformation = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayNavigationInformation.assert_called_with()

    def test_display_should_call_displayQueueViewInformation(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayNavigationInformation = Mock()
        self.test_presenter.displayQueueViewInformation = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayQueueViewInformation.assert_called_with()

    def test_display_should_draw_window_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayNavigationInformation = Mock()
        self.test_presenter.displayQueueViewInformation = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.draw.assert_called_with([])

    def test_display_should_draw_pad_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayNavigationInformation = Mock()
        self.test_presenter.displayQueueViewInformation = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.pad.draw.assert_called_with([])

    def test_display_should_ensure_that_help_screen_never_scrolls(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.window.pad = Mock()
        self.test_presenter.displayNavigationInformation = Mock()
        self.test_presenter.displayQueueViewInformation = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.pad.scrollToLine.assert_called_with(0)

    def test_displayGeneralInformation_should_add_screen_instructions(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.displayNavigationInformation = Mock()
        self.test_presenter.displayQueueViewInformation = Mock()

        self.test_presenter.displayGeneralInformation()

        assert len(self.test_presenter.screen) == 2

    def test_displayNavigationInformation_should_update_pad_with_general_information(self):

        self.test_presenter.displayNavigationInformation()

        assert len(self.test_presenter.pad) == 18

    def test_displayQueueViewInformation_should_update_pad_with_queue_information(self):

        self.test_presenter.displayQueueViewInformation()

        assert len(self.test_presenter.pad) == 9

if __name__ == '__main__':
    nose.runmodule()