from presenters.sabWarningsPresenter import sabWarningsPresenter
import sabAPI


class sabWarningsController():
    def __init__(self, api = None, warningsPresenter = None):
        if not api:
            api = sabAPI.api.api()
        self.api = api

        if not warningsPresenter:
            warningsPresenter = sabWarningsPresenter()
        self.warningsPresenter = warningsPresenter

        self.selected = False
        self.state = {}
        self.index = -1

    def update(self):
        self.state = self.api.listWarnings()
        return self.state

    def display(self):
        self.state["current_index"] = self.index
        self.state["list_length"] = len(self.state["warnings"])
        self.state["item_size"] = 2
        self.warningsPresenter.display(self.state)

    def handleInput(self, keyPressed):
        handled = self.handleItemSelection(keyPressed)

        if not self.selected:
            return handled

        return self.handleItemManipulation(handled, keyPressed)

    def handleItemSelection(self, keyPressed):
        handled = False

        if keyPressed == 259:  # Cursor up
            handled = self.handleUp()

        elif keyPressed == 258:  # Cursor down
            handled = self.handleDown()

        elif keyPressed == 339:  # Page up
            handled = self.handlePageUp()

        elif keyPressed == 338:  # Page down
            handled = self.handlePageDown()

        elif keyPressed == 262:  # Home
            handled = self.handleHome()

        elif keyPressed in (360, 385):  # End
            handled = self.handleEnd()

        self.selected = self.index != -1

        return handled

    def handleItemManipulation(self, handled, keyPressed):
        if keyPressed in ( 330, 263, 127):  # Delete
            handled = self.handleDelete()
        return handled

    def handleDelete(self):
#        if self.index > -1 and self.index < len(self.state["warnings"]):
#            self.api.deleteDownload(self.state["warnings"][self.index]["id"])
        return True

    def handleDown(self):
        if self.index < len(self.state["warnings"]) - 1:
            self.index += 1
        else:
            self.index = -1
        return True

    def handleUp(self):
        if self.index > -1:
            self.index -= 1
        else:
            self.index = len(self.state["warnings"]) - 1
        return True

    def handlePageUp(self):
        if self.index - 5 > -1:
            self.index -= 5
        else:
            self.index = -1
        return True

    def handlePageDown(self):
        maxListIndex = len(self.state["warnings"]) - 1
        if self.index + 5 <= maxListIndex:
            self.index += 5
        else:
            self.index = maxListIndex
        return True

    def handleHome(self):
        self.index = 0
        return True

    def handleEnd(self):
        self.index = len(self.state["warnings"]) - 1
        return True