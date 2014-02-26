import sys

class sabHistoryController( object ):

    def __init__(self):
        self.api = sys.modules["__main__"].api
        self.historyPresenter = sys.modules["__main__"].historyPresenter
        self.selected = False
        self.state = {}

    def update(self):
        self.state = self.api.listHistory()
        return self.state

    def display(self):
        self.historyPresenter.display(self.state)

    def handleInput(self, keyPressed):
        return False