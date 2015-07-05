import nose
import BaseTestCase
from mock import Mock
from cursesUI.cursesWindow import cursesWindow
from presenters.sabMiscPresenter import sabMiscPresenter
from presenters.sabScrollPresenter import sabScrollPresenter


class sabMiscPresenter_Test(BaseTestCase.BaseTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.test_presenter = sabMiscPresenter(window=Mock(spec=cursesWindow),
                                               scrollPresenter=Mock(spec=sabScrollPresenter))

    def test_should_instantiate(self):
        assert (isinstance(self.test_presenter, sabMiscPresenter))

    def test_display_should_call_displayGeneralInformation(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayMiscellaneousInformation = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayGeneralInformation.assert_called_with({"item_size": 3})

    def test_display_should_call_displayMiscellaneousInformation(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayMiscellaneousInformation = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayMiscellaneousInformation.assert_called_with({"item_size": 3})

    def test_display_should_draw_window_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayMiscellaneousInformation = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.draw.assert_called_with([])

    def test_display_should_draw_pad_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayMiscellaneousInformation = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.pad.draw.assert_called_with([])

    def test_display_should_call_scrollPresenter(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayMiscellaneousInformation = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.scrollPresenter.display({})

    def test_displayGeneralInformation_should_add_screen_instructions(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.displayNavigationInformation = Mock()
        self.test_presenter.displayQueueViewInformation = Mock()

        self.test_presenter.displayGeneralInformation({"version": "1.0.0"})

        assert len(self.test_presenter.screen) == 3

    def test_displayMiscellaneousInformation_should_update_pad_with_general_information(self):
        self.test_presenter.displayMiscellaneousInformation({"speedlimit": "300"})

        assert len(self.test_presenter.pad) == 19


if __name__ == '__main__':
    nose.runmodule()