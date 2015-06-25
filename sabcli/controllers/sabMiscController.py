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
        self.cached = False
        self.selectedItem = -1

    def update(self):
        self.state = self.api.getApiInfo()
        self.state["list_length"] = 6
        return self.state

    def display(self):
        self.state["current_index"] = self.selectedItem
        self.state["list_length"] = self.selectedItem
        self.miscPresenter.display(self.state)

    def handleInput(self, keyPressed):
        handled = False

        if not self.selected:
            return handled

        elif keyPressed == 259:  # Cursor up
            handled = self.handleUp()

        elif keyPressed == 258:  # Cursor down
            handled = self.handleDown()

        elif keyPressed == 260:  # Left
            handled = self.handleLeft()

        elif keyPressed == 261:  # Right
            handled = self.handleRight()

        self.selected = self.selectedItem != -1
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

    def handleLeft(self):
        self.selected = False
        return False

    def handleRight(self):
        self.selected = False
        return False
