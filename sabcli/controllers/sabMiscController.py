from presenters.sabMiscPresenter import sabMiscPresenter
import sabAPI


class sabMiscController():
    def __init__(self, api = None, miscPresenter = None):
        if not api:
            api = sabAPI.api.api()
        self.api = api

        if not miscPresenter:
            miscPresenter = sabMiscPresenter()
        self.miscPresenter = miscPresenter

        self.selected = False
        self.cached = False

    def update(self):
        self.state = self.api.getApiInfo()
        return self.state

    def display(self):
        self.miscPresenter.display(self.state)

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