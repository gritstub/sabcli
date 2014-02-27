import sys, time

class sabNavigationController():

    def __init__(self):
        self.navigation = sys.modules["__main__"].navigationPresenter
        self.status = {}
        self.view_strings = [('[1-Queue]', 0), (' [2-History]', 1), (' [3-Warnings]', 2), (' [4-More]', 3), (' [5-Help]', 4)]

    def updateSpeed(self, state):
        if "status" not in state:
            return

        if state['status'] == 'Paused':
            self.status["speed"] = "Paused"
        else:
            self.status["speed"] = state["speed"]

    def updateSelectedView(self, selected_view):
        views = []
        for name, index in self.view_strings:
            selected = index == selected_view
            views.append((name, selected))
        self.status["views"] = views

    def update(self, selected_view, state = {}):
        self.updateSpeed(state)
        self.updateSelectedView(selected_view)


    def display(self):
        self.navigation.display(self.status)