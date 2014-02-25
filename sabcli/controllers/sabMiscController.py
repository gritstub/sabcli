import sys

class sabMiscController():

    def __init__(self):
        self.api = sys.modules["__main__"].api
        self.miscPresenter = sys.modules["__main__"].miscPresenter
        self.selected = False

        self.cached = False

    def update(self):
        pass

    def display(self):
        self.miscPresenter.display({}) # TODO: get version information to pass on to presenter

    def handleInput(self, keyPressed):
        handled = False

        if not self.selected:
            return handled

        elif keyPressed == 259: # Curser up
            handled = self.handleUp(handled)

        elif keyPressed == 258:  # Curser down
            handled = self.handleDown(handled)

        return handled

    def handleDown(self, handled):
        return handled

    def handleUp(self, handled):
        return handled