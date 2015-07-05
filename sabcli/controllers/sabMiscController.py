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

        self.item_length = 6
        self.selected = False

        self.selectedItem = -1

    def update(self):
        self.state = self.api.getApiInfo()
        return self.state

    def display(self):
        self.state["current_index"] = self.selectedItem
        self.state["list_length"] = 6
        self.miscPresenter.display(self.state)

    def handleInput(self, keyPressed):
        handled = False

        if keyPressed == 259:  # Cursor up
            handled = self.handleUp()

        elif keyPressed == 258:  # Cursor down
            handled = self.handleDown()

        if not self.selected:
            return handled

        return handled

    def handleUp(self):
        if self.selectedItem > -1:
            self.selectedItem -= 1
        else:
            self.selectedItem = self.item_length - 1
        return True

    def handleDown(self):
        if self.selectedItem < self.item_length - 1:
            self.selectedItem += 1
        else:
            self.selectedItem = -1
        return True