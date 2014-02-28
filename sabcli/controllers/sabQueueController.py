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
            handled = self.handleUp(handled)

        elif keyPressed == 258:  # Curser down
            handled = self.handleDown(handled)

        elif keyPressed == 339: # Page up
            handled = self.handlePageUp(handled)

        elif keyPressed == 338: # Page down
            handled = self.handlePageDown(handled)

        elif keyPressed == 262: # Home
            handled = self.handleHome(handled)

        elif keyPressed in ( 360, 385 ): # end
            handled = self.handleEnd(handled)

        return handled

    def handlePageUp(self, handled):
        handled = True
        if sabnzbd.index[sabnzbd.view] - 5 > -1:
            sabnzbd.index[sabnzbd.view] = sabnzbd.index[sabnzbd.view] - 5
        else:
            sabnzbd.index[sabnzbd.view] = -1
        return handled

    def handlePageDown(self, handled):
        handled = True
        if sabnzbd.index[sabnzbd.view] == -1:
            if sabnzbd.indexCount[sabnzbd.view] >= 5:
                sabnzbd.index[sabnzbd.view] = 5
            else:
                sabnzbd.index[sabnzbd.view] = sabnzbd.indexCount[sabnzbd.view]
        elif sabnzbd.index[sabnzbd.view] + 5 <= sabnzbd.indexCount[sabnzbd.view]:
            sabnzbd.index[sabnzbd.view] = sabnzbd.index[sabnzbd.view] + 5
        else:
            sabnzbd.index[sabnzbd.view] = sabnzbd.indexCount[sabnzbd.view]
        return handled

    def handleHome(self, handled):
        sabnzbd.index[sabnzbd.view] = -1
        handled = True
        return handled

    def handleEnd(self, handled):
        sabnzbd.index[sabnzbd.view] = sabnzbd.indexCount[sabnzbd.view]
        handled = True
        return handled

    def handleDown(self, handled):
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

    def handleUp(self, handled):
        if self.selection == -1:
            if self.index > -1:
                self.index -= 1
                handled = True
        if self.selection == 1 and self.details['priority'][self.index[0]] < 2:
            self.details['priority'][self.index[0]] += 1
            handled = True
            # self.action = 11 # TODO: replace with call to api
        if self.selection == 2 and self.details['unpackopts'][self.index[0]] > 0:
            self.details['unpackopts'][self.index[0]] -= 1
            handled = True
            #self.action = 12 # TODO: replace with call to api
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