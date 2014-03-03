import sys

class sabWarningsController( object ):

    def __init__(self):
        self.api = sys.modules["__main__"].api
        self.warningsPresenter = sys.modules["__main__"].warningsPresenter
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

        self.selected = self.index != -1
        return handled

    def handleDelete(self):
        if self.index > -1 and self.index < len(self.state["warnings"]):
            self.api.deleteDownload(self.state["warnings"][self.index]["id"])
        return True

    def handleDown(self):
        if self.index < len(self.state["warnings"]) -1:
            self.index += 1
        else:
            self.index = -1
        return True

    def handleUp(self):
        if self.index > -1:
            self.index -= 1
        else:
            self.index = len(self.state["warnings"]) -1
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