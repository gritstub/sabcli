import sys

class sabHistoryController( object ):

    def __init__(self):
        self.api = sys.modules["__main__"].api
        self.historyPresenter = sys.modules["__main__"].historyPresenter
        self.selected = False
        self.index = -1
        self.state = {}

    def update(self):
        self.state = self.api.listHistory()
        return self.state

    def display(self):
        self.state["current_index"] = self.index
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

        elif keyPressed == 339: # Page up
            handled = self.handlePageUp()

        elif keyPressed == 338: # Page down
            handled = self.handlePageDown()

        elif keyPressed == 262: # Home
            handled = self.handleHome()

        elif keyPressed in ( 360, 385 ): # end
            handled = self.handleEnd()

        return False

    def handleDelete(self):
        if self.index > -1 and self.index < len(self.state["queue"]):
            self.api.deleteDownload(self.state["queue"][self.index]["id"])
        return True

    def handleDown(self):
        if self.index < len(self.state["history"]) -1:
            self.index += 1
        else:
            self.index = -1
            self.selected = False
        return True

    def handleUp(self):
        if self.index > -1:
            self.index -= 1
        else:
            self.index = len(self.state["history"]) -1
            self.selected = True
        if self.index == -1:
            self.selected = False
        return True

    def handlePageUp(self):
        handled = True
        if self.index - 5 > -1:
            self.index -= 5
        else:
            self.index = -1
        return handled

    def handlePageDown(self):
        maxListIndex = len(self.state["history"]) - 1
        if self.index + 5 <= maxListIndex:
            self.index += 5
        else:
            self.index = maxListIndex
        return True

    def handleHome(self):
        self.index = 0
        return True

    def handleEnd(self):
        self.index = len(self.state["history"]) - 1
        return True
