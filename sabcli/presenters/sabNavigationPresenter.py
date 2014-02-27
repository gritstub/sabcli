import curses, sys

class sabNavigationPresenter():

    def __init__(self):
        self.window = sys.modules["__main__"].window

    def displaySpeed(self, state = {}):
        if 'speed' not in state:
            return

        try:
            self.window.addString(0, int(self.window.size[1]) - 7 - len(state['speed']), 'Speed: ')
        except:
            pass

        try:
            self.window.addString(0, int(self.window.size[1]) - len(state['speed']), state['speed'], curses.color_pair(7))
        except:
            pass

    def displayNavigation(self, state):
        if 'views' not in state:
            return

        self.window.addString(0, 0, '')

        for name, selected_view in state["views"]:
            if selected_view:
                self.window.addStr(name, curses.color_pair(7))
            else:
                self.window.addStr(name)

    def display(self, state = {}):
        self.displayNavigation(state)
        self.displaySpeed(state)