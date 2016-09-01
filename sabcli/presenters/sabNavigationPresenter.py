from cursesUI.cursesWindow import cursesWindow


class sabNavigationPresenter():
    def __init__(self, window = None):
        if not window:
            window = cursesWindow()
        self.window = window
        self.screen = []

    def display(self, state):
        self.screen = []

        self.displayNavigation(state)
        self.displaySpeed(state)

        self.window.draw(self.screen)

    def displayNavigation(self, state):
        if "views" not in state:
            return

        index = 0
        for name, selected_view in state["views"]:
            if selected_view:
                self.screen.append((index, 0, name, 4))
            else:
                self.screen.append((index, 0, name, ''))
            index += len(name)

    def displaySpeed(self, state = {}):
        if "speed" not in state:
            return

        self.screen.append((int(self.window.size[1]) - 7 - len(state["speed"]), 0, "Speed: ", ""))
        self.screen.append((int(self.window.size[1]) - len(state["speed"]), 0, state["speed"], 7))

    # TODO: remove this, since we don't test in production
    def displayKeyPress(self, key_press):
        self.screen = []
        self.screen.append((int(self.window.size[1]) - len(key_press), 1, key_press, ""))
        self.window.draw(self.screen)
        self.window.refresh()
        self.window.update()
