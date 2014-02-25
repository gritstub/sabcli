import sys

class sabWarningsController( object ):

    def __init__(self):
        self.api = sys.modules["__main__"].api
        self.warningsPresenter = sys.modules["__main__"].warningsPresenter
        self.selected = False
        self.state = {}

    def update(self):
        self.state = self.api.listWarnings()
        return self.state

    def display(self):
        self.warningsPresenter.display(self.state)

    def handleInput(self, keyPressed):
        return False