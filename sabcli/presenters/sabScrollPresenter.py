from cursesUI.cursesWindow import cursesWindow


class sabScrollPresenter():
    def __init__(self, window = None):
        if not window:
            window = cursesWindow()
        self.window = window

        self.item_size = 0

        self.screen = []
        self.pad = []

    def display(self, state):
        self.screen = []
        self.pad = []

        self.item_size = state.get("item_size", 3)
        self.max_window_items = int((int(self.window.size[0]) - 6) / self.item_size)

        self.displaySelectedItem(state)
        self.displayScrollBar(state)

        self.window.draw(self.screen)
        self.window.pad.draw(self.pad)

    def displaySelectedItem(self, state):
        if state["current_index"] < 0:
            return

        start = state["current_index"] * self.item_size
        for i in range(self.item_size - 1):
            self.pad.append((0, i + start, '*', ''))

    def displayScrollBar(self, state):
        if state["list_length"] <= self.max_window_items:
            return

        current_index = state["current_index"]
        if state["current_index"] < 0:
            current_index = 0

        progress_bar_length = int(self.window.size[0]) - 5
        scroll_bar_line_position = int(progress_bar_length * (float(current_index) / float(state["list_length"])))

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

''' TODO: This presenter contains to much logic to calculate what needs to be updated on
    screen, this data needs to be prepared by a view controller '''

'''
    def scrollViewPort(self, state):
        center_item = int(self.max_window_items / 2)

        if state["current_index"] > center_item - 1 and state["current_index"] < state["list_length"] - center_item:
            self.centerViewOnSelectedItem(center_item, state)

        elif state["current_index"] >= state["list_length"] - center_item:
            self.goToLastScreenInList(center_item, state)

    def centerViewOnSelectedItem(self, center_item, state):
        first_line_where_selected_item_is_centered = (state["current_index"] - center_item) * self.item_size
        #self.window.pad.scrollToLine(first_line_where_selected_item_is_centered)

    def goToLastScreenInList(self, center_item, state):
        first_line_of_last_screen = (state["list_length"] - (center_item * 2)) * self.item_size
        #self.window.pad.scrollToLine(first_line_of_last_screen)
'''