from cursesUI.cursesWindow import cursesWindow


class sabFlexibleScrollPresenter():
    def __init__(self, window = None):
        if not window:
            window = cursesWindow()
        self.window = window

        self.item_size = 0

        self.max_window_size = int(self.window.size[0]) - 5
        self.window_center_point = int((float(self.window.size[0]) - 5) / 2)

        self.screen = []
        self.pad = []

    def display(self, state):
        self.screen = []
        self.pad = []

        self.displaySelectedItem(state)
        self.displayScrollBar(state)

        self.window.draw(self.screen)
        self.window.pad.draw(self.pad)

        self.scrollViewPort(state)

    def displaySelectedItem(self, state):
        if state["current_index"] < 0 or "item_lengths" not in state:
            return

        start = state["selected_item_start"]
        self.item_size = state["item_lengths"][state["current_index"]]

        for i in range(self.item_size):
            self.pad.append((0, i + start, '*', ''))

    def displayScrollBar(self, state):
        if state["list_length"] <= self.max_window_size:
            return

        progress_bar_length = int(self.window.size[0]) - 5
        scroll_bar_line_position = int(progress_bar_length * (float(state["selected_item_start"]) / float(state["list_length"])))

        if scroll_bar_line_position == 0:
            scroll_bar_line_position = 1

        self.drawProgressBar(progress_bar_length, scroll_bar_line_position)

    def drawProgressBar(self, progress_bar_length, scroll_bar_line_position):
        current_line = 0
        screen_right_side = int(self.window.size[1]) - 1

        while current_line < progress_bar_length:
            if current_line < scroll_bar_line_position - 1 or current_line > scroll_bar_line_position + 1:
                self.screen.append((screen_right_side, current_line + 4, '|', ''))
            else:
                self.screen.append((screen_right_side, current_line + 4, '#', ''))
            current_line += 1

    def scrollViewPort(self, state):
        if state["list_length"] < self.max_window_size:
            self.window.pad.scrollToLine(0)
        elif state["selected_item_start"] > self.window_center_point - 1 and state["selected_item_start"] < state["list_length"] - self.window_center_point:
            self.centerViewOnSelectedItem(self.window_center_point, state)
        elif state["selected_item_start"] >= state["list_length"] - self.window_center_point:
            self.goToLastScreenInList(self.window_center_point, state)
        else:
            self.window.pad.scrollToLine(0)

    def centerViewOnSelectedItem(self, center_item, state):
        first_line_where_selected_item_is_centered = (state["selected_item_start"] + state["item_lengths"][state["current_index"]] - center_item)
        self.window.pad.scrollToLine(first_line_where_selected_item_is_centered)

    def goToLastScreenInList(self, center_item, state):
        first_line_of_last_screen = state["list_length"] - (center_item * 2)
        self.window.pad.scrollToLine(first_line_of_last_screen)