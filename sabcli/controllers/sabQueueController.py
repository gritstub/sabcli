import sys

class sabQueueController():

    def __init__(self):
        self.api = sys.modules["__main__"].api
        self.queuePresenter = sys.modules["__main__"].queuePresenter

        self.selected = False

        self.state = {}

        self.index = -1
        self.selection = -1

    def update(self):
        self.state = self.api.listQueue()
        return self.state

    def display(self):
        self.queuePresenter.display(self.state)

    def handleInput(self, keyPressed):
        handled = False

        if not self.selected:
            return handled

        elif keyPressed == ord('p'): # pause
            handled = self.handlePause()

        elif keyPressed == ord('r'): # resume
            handled = self.handleResume()

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

        elif keyPressed == 260: # Left
            handled = self.handleLeft()

        elif keyPressed == 261: # Right
            handled = self.handleRight()

        elif keyPressed == 262: # Home
            handled = self.handleHome()

        elif keyPressed in ( 360, 385 ): # end
            handled = self.handleEnd()

        return handled

    def handlePageUp(self):
        handled = True
        if self.index[self.view] - 5 > -1:
            self.index[self.view] = self.index[self.view] - 5
        else:
            self.index[self.view] = -1
        return handled

    def handlePageDown(self):
        handled = True
        if self.index[self.view] == -1:
            if self.indexCount[self.view] >= 5:
                self.index[self.view] = 5
            else:
                self.index[self.view] = self.indexCount[self.view]
        elif self.index[self.view] + 5 <= self.indexCount[self.view]:
            self.index[self.view] = self.index[self.view] + 5
        else:
            self.index[self.view] = self.indexCount[self.view]
        return handled

    def handleHome(self):
        self.index = 0
        return True

    def handleEnd(self):
        self.index = len(self.state["queue"]) - 1
        return True

    def handleDown(self):
        if self.selection == -1:
            if self.index < 20: # TODO find max limit based on state:
                self.index += 1
                handled = True
        if self.selection == 1 and self.details['priority'][self.index[0]] > -1:
            self.details['priority'][self.index[0]] -= 1
            #self.action = 11 # TODO: replace with call to api
            handled = True
        if self.selection == 2 and self.details['unpackopts'][self.index[0]] < 3:
            self.details['unpackopts'][self.index[0]] += 1
            #self.action = 12 # TODO: replace with call to api
            handled = True
        return handled

    def handleUp(self):
        if self.selection == -1:
            if self.index > -1:
                self.index -= 1
                handled = True
        if self.selection == 1 and self.state['priority'][self.index[0]] < 2:
            #self.state['priority'] += 1
            handled = True
            # self.action = 11 # TODO: replace with call to api
        if self.selection == 2 and self.details['unpackopts'][self.index[0]] > 0:
            self.state['unpackopts'][self.selected] -= 1
            handled = True
            #self.action = 12 # TODO: replace with call to api
        return handled

    def handleLeft(self):
        handled = False
        return handled

    def handleRight(self):
        handled = False
        return handled

    def handleDelete(self):
        #self.api.
        #self.action = 6 # TODO: replace with call to api
        return True

    def handleResume(self):
        #self.action = 5 # TODO: replace with call to api
        return True

    def handlePause(self):
        #self.action = 4 # TODO: replace with call to api
        return True