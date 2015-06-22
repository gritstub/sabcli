import nose
import BaseTestCase
from mock import Mock
from cursesUI import cursesWindow
from presenters.sabScrollPresenter import sabScrollPresenter


class sabScrollPresenter_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.test_presenter = sabScrollPresenter(window=Mock(spec=cursesWindow.cursesWindow))

    def test_should_instantiate(self):
        assert(isinstance(self.test_presenter, sabScrollPresenter))

    def test_display_should_call_displaySelectedItem(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.displaySelectedItem = Mock()
        self.test_presenter.displayScrollBar = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displaySelectedItem.assert_called_with({})

    def test_display_should_call_displayScrollBar(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.displaySelectedItem = Mock()
        self.test_presenter.displayScrollBar = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayScrollBar.assert_called_with({})

    def test_display_should_draw_window_instructions(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.displaySelectedItem = Mock()
        self.test_presenter.displayScrollBar = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.draw.assert_called_with([])

    def test_display_should_draw_pad_instructions(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.displaySelectedItem = Mock()
        self.test_presenter.displayScrollBar = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.pad.draw.assert_called_with([])

    def test_displaySelectedItem_should_not_add_pad_instructions_if_current_index_negative(self):

        self.test_presenter.displaySelectedItem({"current_index": -1})

        assert len(self.test_presenter.pad) == 0

    def test_displaySelectedItem_should_add_pad_instructions_if_current_index_is_not_negative(self):
        self.test_presenter.item_size = 4

        self.test_presenter.displaySelectedItem({"current_index": 0})

        assert len(self.test_presenter.pad) == 3

    def test_displayScrollBar_should_calculate_scrollbar_dimension_correctly(self):
        self.test_presenter.item_size = 4
        self.test_presenter.max_window_items = 2
        self.test_presenter.window.size = ["20", "20"]
        self.test_presenter.drawProgressBar = Mock()

        self.test_presenter.displayScrollBar({"current_index": 0, "list_length": 3})

        self.test_presenter.drawProgressBar.assert_called_with(15, 1)

    def test_displayScrollBar_should_not_drawProgressBar_if_items_fit_on_screen(self):
        self.test_presenter.item_size = 4
        self.test_presenter.max_window_items = 5
        self.test_presenter.drawProgressBar = Mock()

        self.test_presenter.displayScrollBar({"list_length": 3})

        assert not self.test_presenter.drawProgressBar.called

    def test_drawProgressBar_should_add_screen_instructions(self):
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.drawProgressBar(15, 1)

        assert len(self.test_presenter.screen) == 15

if __name__ == '__main__':
    nose.runmodule()