from controllers.sabDownloadQueueController import sabDownloadQueueController
from controllers.sabDownloadDetailsController import sabDownloadDetailsController
import sabAPI


class sabDownloadController():
    def __init__(self, api = None, downloadQueue = None, downloadDetails = None):
        if not api:
            api = sabAPI.api.api()
        self.api = api

        if not downloadQueue:
            downloadQueue = sabDownloadQueueController()
        self.downloadQueue = downloadQueue

        if not downloadDetails:
            downloadDetails = sabDownloadDetailsController()
        self.downloadDetails = downloadDetails

        self.controllers = [downloadQueue, downloadDetails]
        self.selectedControllerIndex = 0
        self.currentController = self.controllers[self.selectedControllerIndex]
        self.selected = False
        self.state = {}

    def update(self):
        if self.selectedControllerIndex == 1:
            self.state = self.currentController.update(self.downloadQueue.getSelectedItemId())
            return self.state
        else:
            self.state = self.currentController.update()
            return self.state

    def display(self):
        self.currentController.display()

    def handleInput(self, keyPressed):
        handled = False

        if self.currentController.handleInput(keyPressed):
            self.selected = self.currentController.selected
            return True

        elif keyPressed == ord('d'):  # Pause
            handled = self.handleDownloadDetailsRequest()

        return handled

    def handleDownloadDetailsRequest(self):
        if self.selectedControllerIndex == 0:
            self.selectedControllerIndex = 1
        else:
            self.selectedControllerIndex = 0

        self.currentController = self.controllers[self.selectedControllerIndex]

        self.state["dirty"] = True
        return True