import sys

class sabQueueDetailsController():

    def __init__(self):
        self.api = sys.modules["__main__"].api
        self.queueDetailsPresenter = sys.modules["__main__"].queueDetailsPresenter

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