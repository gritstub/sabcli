from presenters.sabHistoryPresenter import sabHistoryPresenter
import sabAPI


class sabHistoryController():
    def __init__(self, api = None, historyPresenter = None):
        if not api:
            api = sabAPI.api.api()
        self.api = api

        if not historyPresenter:
            historyPresenter = sabHistoryPresenter()
        self.historyPresenter = historyPresenter

        self.selected = False
        self.selectedItem = -1
        self.state = {}

    def update(self):
        self.state = self.api.listHistory()
        return self.state

    def display(self):
        self.state["current_index"] = self.selectedItem
        self.state["item_size"] = 2
        self.state["list_length"] = len(self.state["history"])
        self.historyPresenter.display(self.state)

    def handleInput(self, keyPressed):
        handled = False

        if not self.selected:
            return handled

        elif keyPressed in ( 330, 263, 127): # delete #263 (backspace linux) #127 (backspace freebsd) 330 (delete freebsd/linux)
            handled = self.handleDelete()

        elif keyPressed == 259: # Curser up
            handled = self.handleUp()

        elif keyPressed == 258:  # Curser down
            handled = self.handleDown()

        elif keyPressed == 260: # Left
            handled = True

        elif keyPressed == 261: # Right
            handled = True

        elif keyPressed == 339: # Page up
            handled = self.handlePageUp()

        elif keyPressed == 338: # Page down
            handled = self.handlePageDown()

        elif keyPressed == 262: # Home
            handled = self.handleHome()

        elif keyPressed in ( 360, 385 ): # end
            handled = self.handleEnd()

        self.selected = self.selectedItem != -1
        return handled

    def handleDelete(self):
        if self.selectedItem > -1 and self.selectedItem < len(self.state["history"]):
            self.api.deleteDownload(self.state["history"][self.selectedItem]["id"])
        return True

    def handleDown(self):
        if self.selectedItem < len(self.state["history"]) -1:
            self.selectedItem += 1
        else:
            self.selectedItem = -1
        return True

    def handleUp(self):
        if self.selectedItem > -1:
            self.selectedItem -= 1
        else:
            self.selectedItem = len(self.state["history"]) -1
        return True

    def handlePageUp(self):
        if self.selectedItem - 5 > -1:
            self.selectedItem -= 5
        else:
            self.selectedItem = -1
        return True

    def handlePageDown(self):
        maxListIndex = len(self.state["history"]) - 1
        if self.selectedItem + 5 <= maxListIndex:
            self.selectedItem += 5
        else:
            self.selectedItem = maxListIndex
        return True

    def handleHome(self):
        self.selectedItem = 0
        return True

    def handleEnd(self):
        self.selectedItem = len(self.state["history"]) - 1
        return True
