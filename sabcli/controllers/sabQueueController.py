import sys

class sabQueueController():

    def __init__(self):
        self.api = sys.modules["__main__"].api
        self.queuePresenter = sys.modules["__main__"].queuePresenter

        self.selected = False

        self.state = {}

        self.index = -1
        self.selection = -1
        self.priority = ['Low', 'Normal','High','Force','Repair']

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
        if self.index > -1 and self.index < len(self.state["queue"]):
            self.api.resumeDownload(self.state["queue"][self.index]["id"])
        return True

    def handlePause(self):
        if self.index > -1 and self.index < len(self.state["queue"]):
            self.api.pauseDownload(self.state["queue"][self.index]["id"])
        return True

    def handleDelete(self):
        if self.index > -1 and self.index < len(self.state["queue"]):
            self.api.deleteDownload(self.state["queue"][self.index]["id"])
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
        priority_index = self.priority.index(download["priority"])

        if priority_index < 2:
            download["priority"] = self.priority[priority_index + 1]
            self.api.changeDownloadPriority(download["id"], download["priority"])
        return True

    def addDownloadPostPocessingSteps(self, download):
        if download['unpackopts'] < 3:
            self.state['unpackopts'][self.selected] += 1
            self.api.changeDownloadPostProcessing(download["id"], download["unpackopts"])
        return True

    def scrollUp(self):
        if self.index > -1:
            self.index -= 1
        else:
            self.index = len(self.state["queue"]) -1
            self.selected = True
        if self.index == -1:
            self.selected = False
        return True

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
        if self.index < len(self.state["queue"]) -1:
            self.index += 1
        else:
            self.index = -1
            self.selected = False
        return True

    def decreaseDownloadPriority(self, download):
        priority_index = self.priority.index(download["priority"])

        if priority_index > 0:
            download["priority"] = self.priority[priority_index - 1]
            self.api.changeDownloadPriority(download["id"], download["priority"])
        return True

    def removeDownloadProcessingSteps(self, download):
        if download['unpackopts'] > 0:
            download['unpackopts'] -= 1
            self.api.changeDownloadPostProcessing(download["id"], download["unpackopts"])
        return True

    def handleLeft(self):
        if self.index > -1 and self.selection > -1:
            self.selection -= 1
        return True

    def handleRight(self):
        if self.index > -1 and self.selection < 2:
            self.selection +=1
        return True

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