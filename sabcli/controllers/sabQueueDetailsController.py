import sabAPI


class sabQueueDetailsController():
    def __init__(self, api = None, queueDetailsPresenter = None):
        if not api:
            api = sabAPI.api.api()
        self.api = api

        self.queueDetailsPresenter = queueDetailsPresenter

        self.selected = False

        self.state = {}

    def update(self):
        self.state = self.api.listQueue()

    def display(self):
        self.queueDetailsPresenter.display(self.state)

    def handleInput(self, keyPressed):
        handled = False

        if not self.selected:
            return handled

        return handled