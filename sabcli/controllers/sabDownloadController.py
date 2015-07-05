from presenters.sabQueuePresenter import sabQueuePresenter
import sabAPI


class sabQueueController():
    def __init__(self, api = None, queuePresenter = None):
        if not api:
            api = sabAPI.api.api()
        self.api = api

        if not queuePresenter:
            queuePresenter = sabQueuePresenter()
        self.queuePresenter = queuePresenter

        self.selected = False
        self.state = {}
        self.selectedItem = -1
        self.selectedProperty = -1

        self.priority = ['Low', 'Normal', 'High', 'Force', 'Repair']

    def update(self):
        self.state = self.api.listQueue()
        return self.state

    def display(self):
        self.state["current_index"] = self.selectedItem
        self.state["current_selection"] = self.selectedProperty
        self.state["list_length"] = len(self.state["queue"])
        self.queuePresenter.display(self.state)

    def handleInput(self, keyPressed):
        handled = False

        if not self.selected:
            return handled

        elif keyPressed == ord('p'):  # Pause
            handled = self.handlePause()

        elif keyPressed == ord('r'):  # Resume
            handled = self.handleResume()

        elif keyPressed in (330, 263, 127):  # Delete
            handled = self.handleDelete()

        elif keyPressed == 259:  # Cursor up
            handled = self.handleUp()

        elif keyPressed == 258:  # Cursor down
            handled = self.handleDown()

        elif keyPressed == 260:  # Left
            handled = self.handleLeft()

        elif keyPressed == 261:  # Right
            handled = self.handleRight()

        elif keyPressed == 339:  # Page up
            handled = self.handlePageUp()

        elif keyPressed == 338:  # Page down
            handled = self.handlePageDown()

        elif keyPressed == 262:  # Home
            handled = self.handleHome()

        elif keyPressed in (360, 385):  # End
            handled = self.handleEnd()

        elif keyPressed == 10:  # Enter
            handled = self.handleEnter()

        self.selected = self.selectedItem != -1
        return handled

    def handleResume(self):
        if self.selectedItem > -1 and self.selectedItem < len(self.state["queue"]):
            self.api.resumeDownload(self.state["queue"][self.selectedItem]["id"])
            self.state["dirty"] = True
        return True

    def handlePause(self):
        if self.selectedItem > -1 and self.selectedItem < len(self.state["queue"]):
            self.api.pauseDownload(self.state["queue"][self.selectedItem]["id"])
            self.state["dirty"] = True
        return True

    def handleDelete(self):
        if self.selectedItem > -1 and self.selectedItem < len(self.state["queue"]):
            self.api.deleteDownload(self.state["queue"][self.selectedItem]["id"])
            self.state["dirty"] = True
        return True

    def handleUp(self):
        handled = False

        if self.selectedProperty == -1:
            handled = self.scrollUp()
        if self.selectedProperty == 1:
            download = self.state["queue"][self.selectedItem]
            handled = self.increaseDownloadPriority(download)
            self.state["dirty"] = True
        if self.selectedProperty == 2:
            download = self.state["queue"][self.selectedItem]
            handled = self.addDownloadPostPocessingSteps(download)
            self.state["dirty"] = True

        return handled

    def increaseDownloadPriority(self, download):
        priority_index = self.priority.index(download["priority"])

        if priority_index < 4:
            download["priority"] = self.priority[priority_index + 1]
            self.api.changeDownloadPriority(download["id"], priority_index)
            self.state["dirty"] = True

        return True

    def addDownloadPostPocessingSteps(self, download):

        if download['unpackopts'] < 3:
            download['unpackopts'] += 1
            self.api.changeDownloadProcessingSteps(download["id"], download["unpackopts"])
            self.state["dirty"] = True

        return True

    def scrollUp(self):
        if self.selectedItem > -1:
            self.selectedItem -= 1
        else:
            self.selectedItem = len(self.state["queue"]) - 1
        return True

    def handleDown(self):
        handled = False

        if self.selectedProperty == -1:
            handled = self.scrollDown()
        if self.selectedProperty == 1:
            download = self.state["queue"][self.selectedItem]
            handled = self.decreaseDownloadPriority(download)
            self.state["dirty"] = True
        if self.selectedProperty == 2:
            download = self.state["queue"][self.selectedItem]
            handled = self.removeDownloadProcessingSteps(download)
            self.state["dirty"] = True

        return handled

    def scrollDown(self):
        if self.selectedItem < len(self.state["queue"]) - 1:
            self.selectedItem += 1
        else:
            self.selectedItem = -1
        return True

    def decreaseDownloadPriority(self, download):
        priority_index = self.priority.index(download["priority"])

        if priority_index > 0:
            download["priority"] = self.priority[priority_index - 1]
            self.api.changeDownloadPriority(download["id"], priority_index - 2)
            self.state["dirty"] = True
        return True

    def removeDownloadProcessingSteps(self, download):
        if download['unpackopts'] > 0:
            download['unpackopts'] -= 1
            self.api.changeDownloadProcessingSteps(download["id"], download["unpackopts"])
            self.state["dirty"] = True
        return True

    def handleLeft(self):
        if self.selectedItem > -1 and self.selectedProperty > -1:
            self.selectedProperty -= 1
        return True

    def handleRight(self):
        if self.selectedItem > -1 and self.selectedProperty < 2:
            self.selectedProperty += 1
        return True

    def handlePageUp(self):
        if self.selectedItem - 5 > -1:
            self.selectedItem -= 5
        else:
            self.selectedItem = -1
        return True

    def handlePageDown(self):
        maxListIndex = len(self.state["queue"]) - 1
        if self.selectedItem + 5 <= maxListIndex:
            self.selectedItem += 5
        else:
            self.selectedItem = maxListIndex
        return True

    def handleHome(self):
        self.selectedItem = 0
        return True

    def handleEnd(self):
        self.selectedItem = len(self.state["queue"]) - 1
        return True

    def handleEnter(self):
        if self.selectedItem > -1 and self.selectedItem < len(self.state["queue"]) and self.selectedProperty == 0:
            new_name = self.queuePresenter.editDownloadName(self.selectedItem, self.state)
            if new_name and new_name != self.state["queue"][self.selectedItem]["filename"]:
                self.api.renameDownload(self.state["queue"][self.selectedItem]["id"], new_name)
                self.state["dirty"] = True
            return True
        return False