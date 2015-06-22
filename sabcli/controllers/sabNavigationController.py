from presenters.sabNavigationPresenter import sabNavigationPresenter


class sabNavigationController():
    def __init__(self, navigationPresenter = None):
        if not navigationPresenter:
            navigationPresenter = sabNavigationPresenter()
        self.navigationPresenter = navigationPresenter

        self.status = {}
        self.view_strings = [('[1 - Queue]', 0), (' [2 - History]', 1), (' [3 - Warnings]', 2), (' [4 - More]', 3), (' [5 - Help]', 4)]

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

    def displayKeyPress(self, key_press):
        self.navigationPresenter.displayKeyPress(key_press)

    def display(self):
        self.navigationPresenter.display(self.status)