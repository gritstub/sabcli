import nose
import BaseTestCase
from mock import Mock
from cursesUI import cursesWindow
from presenters.sabFlexibleScrollPresenter import sabFlexibleScrollPresenter


class sabFlexibleScrollPresenter_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        cwindow = Mock(spec=cursesWindow.cursesWindow)
        cwindow.size = ["10", "10"]
        self.test_presenter = sabFlexibleScrollPresenter(window=cwindow)

    def test_should_instantiate(self):
        assert(isinstance(self.test_presenter, sabFlexibleScrollPresenter))

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

    def test_displaySelectedItem_should_not_add_pad_instructions_if_item_lenght_is_not_set(self):

        self.test_presenter.displaySelectedItem({"current_index": 1})

        assert len(self.test_presenter.pad) == 0

    def test_displaySelectedItem_should_add_pad_instructions_if_current_index_is_not_negative(self):

        self.test_presenter.displaySelectedItem({"current_index": 1, "item_lengths": [1, 2, 3, 4], "selected_item_start": 3})

        assert len(self.test_presenter.pad) == 2

    def test_displayScrollBar_should_calculate_scrollbar_dimension_correctly(self):
        self.test_presenter.item_size = 4
        self.test_presenter.max_window_size = 2
        self.test_presenter.window.size = ["20", "20"]
        self.test_presenter.drawProgressBar = Mock()

        self.test_presenter.displayScrollBar({"list_length": 3, "selected_item_start": 0})

        self.test_presenter.drawProgressBar.assert_called_with(15, 1)

    def test_displayScrollBar_should_not_drawProgressBar_if_items_fit_on_screen(self):
        self.test_presenter.item_size = 4
        self.test_presenter.max_window_size = 5
        self.test_presenter.drawProgressBar = Mock()

        self.test_presenter.displayScrollBar({"list_length": 3})

        assert not self.test_presenter.drawProgressBar.called

    def test_drawProgressBar_should_add_screen_instructions(self):
        self.test_presenter.window.size = ["1", "1"]

        self.test_presenter.drawProgressBar(15, 1)

        assert len(self.test_presenter.screen) == 15

    def test_scrollViewPort_should_call_pad_scroll_to_line_if_view_is_at_first_screen(self):
        self.test_presenter.centerViewOnSelectedItem = Mock()
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.window.pad = Mock()
        self.test_presenter.max_window_items = 30

        self.test_presenter.scrollViewPort({"list_length": 8, "selected_item_start": 0})

        self.test_presenter.window.pad.scrollToLine.assert_called_with(0)

    def test_scrollViewPort_should_call_centerViewOnSelectedItem_if_selected_item_is_not_at_end_of_list(self):
        self.test_presenter.centerViewOnSelectedItem = Mock()
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.max_window_items = 2

        self.test_presenter.scrollViewPort({"list_length": 8, "selected_item_start": 3})

        self.test_presenter.centerViewOnSelectedItem.assert_called_with(2, {"list_length": 8, "selected_item_start": 3})


    def test_scrollViewPort_should_call_goToLastScreenInList_if_selected_item_is_at_end_of_list(self):
        self.test_presenter.goToLastScreenInList = Mock()
        self.test_presenter.window.size = ["1", "1"]
        self.test_presenter.max_window_items = 2

        self.test_presenter.scrollViewPort({"list_length": 8, "selected_item_start": 7})

        self.test_presenter.goToLastScreenInList.assert_called_with(2, {"list_length": 8, "selected_item_start": 7})

    def test_centerViewOnSelectedItem_should_calculate_centered_line_correctly(self):
        self.test_presenter.window.pad = Mock()

        self.test_presenter.centerViewOnSelectedItem(1, {"item_lengths": [1, 2, 3, 4], "current_index": 2, "selected_item_start": 4})

        self.test_presenter.window.pad.scrollToLine.assert_called_with(4 + 3 - 1)

    def test_goToLastScreenInList_should_calculate_last_line_correctly(self):
        self.test_presenter.window.pad = Mock()
        self.test_presenter.item_size = 3

        self.test_presenter.goToLastScreenInList(4, {"list_length": 20})

        self.test_presenter.window.pad.scrollToLine.assert_called_with((20 - (4 * 2)))

if __name__ == '__main__':
    nose.runmodule()