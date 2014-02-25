import sys

class sabHelpController( object ):

    def __init__(self):
        self.api = sys.modules["__main__"].api
        self.helpPresenter = sys.modules["__main__"].helpPresenter
        self.selected = False
        self.state = {}

    def update(self):
        pass

    def display(self):
        self.helpPresenter.display()

    def handleInput(self, keyPressed):
        return False