from presenters.sabHelpPresenter import sabHelpPresenter
import sabAPI


class sabHelpController( object ):
    def __init__(self, api = None, helpPresenter = None):
        if not api:
            api = sabAPI.api.api()
        self.api = api

        if not helpPresenter:
            helpPresenter = sabHelpPresenter()
        self.helpPresenter = helpPresenter

        self.selected = False
        self.state = {}

    def update(self):
        return {}

    def display(self):
        self.helpPresenter.display()

    def handleInput(self, keyPressed):
        return False