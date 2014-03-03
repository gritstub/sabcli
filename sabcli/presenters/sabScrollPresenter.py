import sys

class sabScrollPresenter( object ):

    def __init__(self):
        self.window = sys.modules["__main__"].window
        self.item_size = 0

    def display(self, state, item_positions = []):
        self.item_size = state.get("item_size", 3)
        self.max_window_items = int((int(self.window.size[0]) - 6) / self.item_size)

        self.displaySelectedItem(state)
        self.displayScrollBar(state)
        self.scrollViewPort(state)

    def displaySelectedItem(self, state):
        if state["current_index"] > -1:
            start = state["current_index"] * self.item_size
            for i in range(self.item_size - 1):
                self.window.pad.addString(i + start, 0, '*')

    def displayScrollBar(self, state):
        if state["current_index"] > -1 and state["list_length"] > self.max_window_items:
            progress_bar_length = int(self.window.size[0]) - 5
            scroll_bar_line_position = int(progress_bar_length * (float(state["current_index"]) / float(state["list_length"])))

            if scroll_bar_line_position == 0:
                scroll_bar_line_position = 1

            current_line = 0
            while current_line < progress_bar_length:
                if current_line < scroll_bar_line_position - 1 or current_line > scroll_bar_line_position + 1:
                    self.window.addString(current_line + 4, int(self.window.size[1]) - 1, '|')
                else:
                    self.window.addString(current_line + 4, int(self.window.size[1]) - 1, '#')
                current_line += 1

    def scrollViewPort(self, state):
        center_item = int(self.max_window_items / 2)

        if state["current_index"] > center_item - 1 and state["current_index"] < state["list_length"] - center_item:
            self.centerViewOnSelectedItem(center_item, state)

        elif state["current_index"] >= state["list_length"] - center_item:
            self.goToLastScreenInList(center_item, state)

    def centerViewOnSelectedItem(self, center_item, state):
        first_line_where_selected_item_is_centered = (state["current_index"] - center_item) * self.item_size
        self.window.pad.scrollToLine(first_line_where_selected_item_is_centered)

    def goToLastScreenInList(self, center_item, state):
        first_line_of_last_screen = (state["list_length"] - (center_item * 2)) * self.item_size
        self.window.pad.scrollToLine(first_line_of_last_screen)