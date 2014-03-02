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
        self.state["current_index"] = self.index
        self.state["current_selection"] = self.selection
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

        elif keyPressed == 260: # Left
            handled = self.handleLeft()

        elif keyPressed == 261: # Right
            handled = self.handleRight()

        elif keyPressed == 339: # Page up
            handled = self.handlePageUp()

        elif keyPressed == 338: # Page down
            handled = self.handlePageDown()

        elif keyPressed == 262: # Home
            handled = self.handleHome()

        elif keyPressed in ( 360, 385 ): # end
            handled = self.handleEnd()

        return handled

    def handleResume(self):
        #self.action = 5 # TODO: replace with call to api
        return True

    def handlePause(self):
        #self.action = 4 # TODO: replace with call to api
        return True

    def handleDelete(self):
        if self.index > -1 and self.index < len(self.state["queue"]):
            download = self.state["queue"][self.index]
            self.api.deleteDownload(download["id"])
            return True

    def handleUp(self):
        if self.selection == -1:
            handled = self.scrollUp()
        if self.selection == 1:
            download = self.state["queue"][self.index]
            handled = self.increaseDownloadPriority(download)
        if self.selection == 2:
            download = self.state["queue"][self.index]
            handled = self.addDownloadPostPocessingSteps(download)
        return handled

    def increaseDownloadPriority(self, download):
        if download['priority'] < 2:
            download["priority"] += 1
            self.api.changeDownloadPriority(download["id"], download["priority"])
        return True

    def addDownloadPostPocessingSteps(self, download):
        if download['unpackopts'] < 3:
            self.state['unpackopts'][self.selected] += 1
            self.api.changeDownloadPostProcessing(download["id"], download["unpackopts"])
        return True

    def scrollUp(self):
        handled = False
        if self.index > -1:
            self.index -= 1
            handled = True
        if self.index == -1:
            self.selected = False
        return handled

    def handleDown(self):
        handled = False
        if self.selection == -1:
            handled = self.scrollDown()
        if self.selection == 1:
            download = self.state["queue"][self.index]
            handled = self.decreaseDownloadPriority(download)
        if self.selection == 2:
            download = self.state["queue"][self.index]
            handled = self.removeDownloadProcessingSteps(download)
        return handled

    def scrollDown(self):
        handled = False
        if self.index < len(self.state["queue"]) -1:
            self.index += 1
            handled = True
        return handled

    def decreaseDownloadPriority(self, download):
        if download['priority'] > 0:
            download["priority"] -= 1
            self.api.changeDownloadPriority(download["id"], download["priority"])
        return True

    def removeDownloadProcessingSteps(self, download):
        if download['unpackopts'] > 0:
            download['unpackopts'] -= 1
            self.api.changeDownloadPostProcessing(download["id"], download["unpackopts"])
        return True

    def handleLeft(self):
        handled = False
        return handled

    def handleRight(self):
        handled = False
        return handled

    def handlePageUp(self):
        handled = True
        if self.index - 5 > -1:
            self.index -= 5
        else:
            self.index = -1
        return handled

    def handlePageDown(self):
        maxListIndex = len(self.state["queue"]) - 1
        if self.index + 5 <= maxListIndex:
            self.index += 5
        else:
            self.index = maxListIndex
        return True

    def handleHome(self):
        self.index = 0
        return True

    def handleEnd(self):
        self.index = len(self.state["queue"]) - 1
        return True