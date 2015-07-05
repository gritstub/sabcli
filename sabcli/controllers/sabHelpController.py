from presenters.sabHelpPresenter import sabHelpPresenter
import sabAPI


class sabHelpController(object):
    def __init__(self, helpPresenter = None):
        if not helpPresenter:
            helpPresenter = sabHelpPresenter()
        self.helpPresenter = helpPresenter

        self.selected = False

    def update(self):
        return {}

    def display(self):
        self.helpPresenter.display({})

    def handleInput(self, keyPressed):
        return False