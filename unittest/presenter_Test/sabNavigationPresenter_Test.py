import nose
import BaseTestCase
from mock import Mock
from cursesUI import cursesWindow
from presenters.sabNavigationPresenter import sabQueuePresenter


class sabNavigationPresenter_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.test_presenter = sabQueuePresenter(window=Mock(spec=cursesWindow.cursesWindow))

    def test_should_instantiate(self):
        assert(isinstance(self.test_presenter, sabQueuePresenter))

    def test_display_should_call_displayGeneralInformation(self):
        self.test_presenter.displaySpeed = Mock()
        self.test_presenter.displayNavigation= Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displaySpeed.assert_called_with({})

    def test_display_should_call_displayNavigation(self):
        self.test_presenter.displaySpeed = Mock()
        self.test_presenter.displayNavigation= Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayNavigation.assert_called_with({})

    def test_display_should_draw_window_instructions(self):
        self.test_presenter.displaySpeed = Mock()
        self.test_presenter.displayNavigation= Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.draw.assert_called_with([])

    def test_displayNavigation_should_add_screen_instructions_if_views_are_present(self):
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displayNavigation({"views": [("main", 0)]})

        assert len(self.test_presenter.screen) == 1
        assert self.test_presenter.screen[0][3] == ''

    def test_displayNavigation_should_also_add_screen_instructions_if_view_is_selected(self):
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displayNavigation({"views": [("main", 1)]})

        assert len(self.test_presenter.screen) == 1
        assert self.test_presenter.screen[0][3] == 7

    def test_displaySpeed_should_not_add_screen_instructions_if_speed_is_missing(self):
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displaySpeed({})

        assert len(self.test_presenter.screen) == 0

    def test_displaySpeed_should_add_screen_instructions_if_speed_is_given(self):
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displaySpeed({"speed": "90 kb/s"})

        assert len(self.test_presenter.screen) == 2

if __name__ == '__main__':
    nose.runmodule()