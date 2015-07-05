from presenters.sabDownloadDetailsPresenter import sabDownloadDetailsPresenter
import sabAPI


class sabDownloadDetailsController():
    def __init__(self, api = None, downloadDetailsPresenter = None):
        if not api:
            api = sabAPI.api.api()
        self.api = api

        if not downloadDetailsPresenter:
            downloadDetailsPresenter = sabDownloadDetailsPresenter()
        self.downloadDetailsPresenter = downloadDetailsPresenter

        self.selected = False
        self.selectedItem = -1

        self.state = {}

    def update(self, download_id):
        self.state = self.api.listDownloadFiles(download_id)
        return self.state

    def display(self):
        self.state["current_index"] = self.selectedItem
        self.state["list_length"] = len(self.state["files"])
        self.downloadDetailsPresenter.display(self.state)

    def handleInput(self, keyPressed):
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

        self.selected = self.selectedItem != -1
        return handled

    def handleUp(self):
        if self.selectedItem > -1:
            self.selectedItem -= 1
        else:
            self.selectedItem = len(self.state["files"]) - 1

        return True

    def handleDown(self):
        if self.selectedItem < len(self.state["files"]) - 1:
            self.selectedItem += 1
        else:
            self.selectedItem = -1

        return True

    def handlePageUp(self):
        if self.selectedItem - 5 > -1:
            self.selectedItem -= 5
        else:
            self.selectedItem = -1
        return True

    def handlePageDown(self):
        maxListIndex = len(self.state["files"]) - 1
        if self.selectedItem + 5 <= maxListIndex:
            self.selectedItem += 5
        else:
            self.selectedItem = maxListIndex
        return True

    def handleHome(self):
        self.selectedItem = 0
        return True

    def handleEnd(self):
        self.selectedItem = len(self.state["files"]) - 1
        return True
