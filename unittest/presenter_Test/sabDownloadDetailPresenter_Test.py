import nose
import BaseTestCase
from mock import Mock
from cursesUI.cursesWindow import cursesWindow
from presenters.sabDownloadDetailsPresenter import sabDownloadDetailsPresenter
from presenters.sabScrollPresenter import sabScrollPresenter


class sabDownloadDetailPresenter_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.test_presenter = sabDownloadDetailsPresenter(window=Mock(spec=cursesWindow), scrollPresenter=Mock(spec=sabScrollPresenter))

    def test_should_instantiate(self):
        assert(isinstance(self.test_presenter, sabDownloadDetailsPresenter))

    def test_display_should_call_displayGeneralInformation(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayDownloadDetails = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayGeneralInformation.assert_called_with()

    def test_display_should_call_displayQueue(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayDownloadDetails = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayDownloadDetails.assert_called_with({"item_size": 3})

    def test_display_should_draw_window_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayDownloadDetails = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.draw.assert_called_with([])

    def test_display_should_call_scrollpresenter_display(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayDownloadDetails = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.scrollPresenter.display.assert_called_with({"item_size": 3})

    def test_display_should_draw_pad_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayDownloadDetails = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.pad.draw.assert_called_with([])

    def test_display_should_draw_pad_instructions(self):
        self.test_presenter.displayGeneralInformation = Mock()
        self.test_presenter.displayDownloadDetails = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.pad.draw.assert_called_with([])

    def test_displayGeneralInformation_should_add_screen_instructions_if_views_are_present(self):
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displayGeneralInformation()

        assert len(self.test_presenter.screen) == 2

    def test_displayDownloadDetails_should_exit_if_there_are_no_files(self):
        self.test_presenter.displayDownloadFileInformation = Mock()
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displayDownloadDetails({"queue": []})

        assert not self.test_presenter.displayDownloadFileInformation.called

    def test_displayDownloadDetails_should_call_displayDownloadFileInformation(self):
        self.test_presenter.displayDownloadFileInformation = Mock()
        self.test_presenter.displayProgress = Mock()
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.displayDownloadDetails({"current_index": 1, "current_selection": 1, "files": [{"index": 0}]})

        self.test_presenter.displayDownloadFileInformation.assert_called_with({"index": 0})

    def test_displayDownloadFileInformation_should_show_show_id(self):
        self.test_presenter.pad = Mock()

        self.test_presenter.displayDownloadFileInformation({"filename": "test_filename", "id": 1, "status": "active",
                                                            "age": "1 day", "mb": "100", "mbleft": "10"})

        self.test_presenter.pad.append.assert_any_call(("1", 3))

    def test_displayDownloadFileInformation_should_show_filename(self):
        self.test_presenter.pad = Mock()

        self.test_presenter.displayDownloadFileInformation({"filename": "test_filename", "id": 1, "status": "active",
                                                            "age": "1 day", "mb": "100", "mbleft": "10"})

        self.test_presenter.pad.append.assert_any_call(("test_filename\n", ''))

    def test_displayDownloadFileInformation_should_show_age(self):
        self.test_presenter.pad = Mock()

        self.test_presenter.displayDownloadFileInformation({"filename": "test_filename", "id": 1, "status": "active",
                                                            "age": "1 day", "mb": "100", "mbleft": "10"})

        self.test_presenter.pad.append.assert_any_call(("1 day", 2))

    def test_displayDownloadFileInformation_should_highlight_status_if_incomplete(self):
        self.test_presenter.pad = Mock()

        self.test_presenter.displayDownloadFileInformation({"filename": "test_filename", "id": 1, "status": "active",
                                                            "age": "1 day", "mb": "100", "mbleft": "10"})

        self.test_presenter.pad.append.assert_any_call(("active", 2))

    def test_displayDownloadFileInformation_should_show_downloaded(self):
        self.test_presenter.pad = Mock()

        self.test_presenter.displayDownloadFileInformation({"filename": "test_filename", "id": 1, "status": "active",
                                                            "age": "1 day", "mb": "100", "mbleft": "10"})

        self.test_presenter.pad.append.assert_any_call(("90.0", 2))
        self.test_presenter.pad.append.assert_any_call(("/100.0 MB]\n\n", ''))

if __name__ == '__main__':
    nose.runmodule()