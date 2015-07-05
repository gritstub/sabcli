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
        self.test_presenter.scrollViewPort = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displaySelectedItem.assert_called_with({})

    def test_display_should_call_displayScrollBar(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.displaySelectedItem = Mock()
        self.test_presenter.displayScrollBar = Mock()
        self.test_presenter.scrollViewPort = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.displayScrollBar.assert_called_with({})

    def test_display_should_draw_window_instructions(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.displaySelectedItem = Mock()
        self.test_presenter.scrollViewPort = Mock()
        self.test_presenter.displayScrollBar = Mock()
        self.test_presenter.scrollViewPort = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.draw.assert_called_with([])

    def test_display_should_draw_pad_instructions(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.displaySelectedItem = Mock()
        self.test_presenter.displayScrollBar = Mock()
        self.test_presenter.scrollViewPort = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.window.pad.draw.assert_called_with([])

    def test_display_should_scroll_viewport_to_selected_item(self):
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.displaySelectedItem = Mock()
        self.test_presenter.displayScrollBar = Mock()
        self.test_presenter.scrollViewPort = Mock()
        self.test_presenter.window.pad = Mock()

        self.test_presenter.display({})

        self.test_presenter.scrollViewPort.assert_called_with({})

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

    def test_calculateScrollingLine_should_return_0_if_view_is_at_first_screen(self):
        self.test_presenter.centerViewOnSelectedItem = Mock()
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.window.pad = Mock()
        self.test_presenter.max_window_items = 30
        self.test_presenter.item_size = 3

        result = self.test_presenter.calculateScrollingLine({"list_length": 8, "current_index": 0})

        assert result == 0

    def test_calculateScrollingLine_should_call_centerViewOnSelectedItem_if_selected_item_is_not_at_end_of_list(self):
        self.test_presenter.centerViewOnSelectedItem = Mock()
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.max_window_items = 2
        self.test_presenter.item_size = 3

        self.test_presenter.calculateScrollingLine({"list_length": 8, "current_index": 3})

        self.test_presenter.centerViewOnSelectedItem.assert_called_with(1, {"list_length": 8, "current_index": 3})

    def test_calculateScrollingLine_should_call_goToLastScreenInList_if_selected_item_is_at_end_of_list(self):
        self.test_presenter.goToLastScreenInList = Mock()

        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.max_window_items = 2
        self.test_presenter.item_size = 3

        self.test_presenter.calculateScrollingLine({"list_length": 8, "current_index": 7})

        self.test_presenter.goToLastScreenInList.assert_called_with(1, {"list_length": 8, "current_index": 7})

    def test_scrollViewPort_should_call_calculateScrollingLine_to_find_correct_line_to_scroll_to(self):
        self.test_presenter.calculateScrollingLine = Mock(return_value=1)
        self.test_presenter.window.pad = Mock()

        self.test_presenter.scrollViewPort({})

        self.test_presenter.calculateScrollingLine.assert_called_with({})

    def test_scrollViewPort_should_call_pad_correctly(self):
        self.test_presenter.calculateScrollingLine = Mock(return_value=1)
        self.test_presenter.window.pad = Mock()

        self.test_presenter.scrollViewPort({})

        self.test_presenter.window.pad.scrollToLine.assert_called_with(1)

    def test_centerViewOnSelectedItem_should_calculate_centered_line_correctly(self):
        self.test_presenter.item_size = 3

        result = self.test_presenter.centerViewOnSelectedItem(4, {"list_length": 20, "current_index": 10})

        assert result == ((10 - 4) * 3)

    def test_goToLastScreenInList_should_calculate_last_line_correctly(self):
        self.test_presenter.item_size = 3

        result = self.test_presenter.goToLastScreenInList(4, {"list_length": 20, "current_index": 17})

        assert result == ((20 - (4 * 2)) * 3)

if __name__ == '__main__':
    nose.runmodule()