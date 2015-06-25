import time
import configuration
from controllers.sabHelpController import sabHelpController
from controllers.sabHistoryController import sabHistoryController
from controllers.sabMiscController import sabMiscController
from controllers.sabNavigationController import sabNavigationController
from controllers.sabQueueController import sabQueueController
from controllers.sabStatusController import sabStatusController
from controllers.sabWarningsController import sabWarningsController
from cursesUI.cursesWindow import cursesWindow
from sabAPI.api import api


class sabController():
    def __init__(self, sabApi = None, window = None, config = None, navigationController = None, statusController = None,
                 queueController = None, historyController = None, warningsController = None, miscController = None, helpController = None):
        self.initApplicationCore(config, sabApi, window)
        self.initGlobalControllers(navigationController, statusController)
        self.initViewControllers(helpController, historyController, miscController, queueController, warningsController)

        # Internal members
        self.last_fetch = {'state_owner':-1, 'refresh': 10, 'time': time.mktime(time.localtime())}
        self.state = {}
        self.debug = True
        self.quit = 0

    def initApplicationCore(self, config, sabApi, window):
        if not sabApi:
            sabApi = api()
        self.api = sabApi
        if not window:
            window = cursesWindow()
        self.window = window
        if not config:
            config = configuration.configuration()
        self.config = config

    def initGlobalControllers(self, navigationController, statusController):
        if not navigationController:
            navigationController = sabNavigationController()
        self.navigationController = navigationController
        if not statusController:
            statusController = sabStatusController()
        self.status = statusController

    def initViewControllers(self, helpController, historyController, miscController, queueController,
                            warningsController):
        if not queueController:
            queueController = sabQueueController()
        if not historyController:
            historyController = sabHistoryController()
        if not warningsController:
            warningsController = sabWarningsController()
        if not miscController:
            miscController = sabMiscController()
        if not helpController:
            helpController = sabHelpController()
        self.currentController = queueController
        self.controllers = [queueController, historyController, warningsController, miscController, helpController]

    def run(self):
        self.window.initialize()
        self.window.pad.initialize()

        while self.quit == 0:
            self.updateApplicationState()

            self.display()

            self.waitForRefresh()

            self.handleUserEvents()

        self.window.close()

    def updateApplicationState(self):
        refresh = self.last_fetch['state_owner'] != self.controllers.index(self.currentController)
        if refresh or time.mktime(time.localtime()) - self.last_fetch['time'] >= self.last_fetch['refresh']:
            self.last_fetch['time'] = time.mktime(time.localtime())
            self.status.displayFetching()
            self.state = self.currentController.update()
            self.navigationController.update(self.controllers.index(self.currentController), self.state)
            self.status.update(self.state)
            self.last_fetch['state_owner'] = self.controllers.index(self.currentController)
            self.refresh = False

    def display(self):
        self.window.clear()

        self.window.refresh()
        self.navigationController.display()
        self.currentController.display()
        self.status.display()

        self.window.update()
    
    def waitForRefresh(self):
        delay = self.calculateRefreshDelay()
        self.window.wait(delay)

    def handleUserEvents(self):
        keyPressed = self.getUserInput()
        if not self.currentController.selected:
            self.handleInput(keyPressed)

        if self.currentController.selected:
            if not self.currentController.handleInput(keyPressed):
                self.handleInput(keyPressed)

    def handleInput(self, keyPressed):

        # Global App Navigation
        if keyPressed == ord('Q') or keyPressed == ord('q'): # quit
            self.quit = 1

        elif keyPressed == 260:  # Curser left
            current_controller_index = self.controllers.index(self.currentController)
            if current_controller_index > 0:
                current_controller_index -= 1
            else:
                current_controller_index = len(self.controllers) - 1

            self.currentController = self.controllers[current_controller_index]

        elif keyPressed == 261:  # Curser right
            current_controller_index = self.controllers.index(self.currentController)
            if current_controller_index < len(self.controllers) - 1:
                current_controller_index += 1
            else:
                current_controller_index = 0

            self.currentController = self.controllers[current_controller_index]

        elif keyPressed == 258:  # Cursor down
            if not self.currentController.selected:
                self.currentController.selected = True

        elif keyPressed == 259:  # Cursor up
            if not self.currentController.selected:
                self.currentController.selected = True

        # Screen select
        elif keyPressed == ord('1'):  # Queue
            self.currentController = self.controllers[0]
        elif keyPressed == ord('2'):  # History
            self.currentController = self.controllers[1]
        elif keyPressed == ord('3'):  # Warnings
            self.currentController = self.controllers[2]
        elif keyPressed == ord('4'):  # More
            self.currentController = self.controllers[3]
        elif keyPressed == ord('5') or keyPressed == ord('?'): # help
            self.currentController = self.controllers[4]

        # Global server commands
        elif keyPressed == ord('p'):  # pause
            self.api.pauseServer()
        elif keyPressed == ord('r'):  # resume
            self.api.resumeServer()
        elif keyPressed == ord('R'):  # restart
            self.api.restartServer()
        elif keyPressed == ord('S'):  # shutdown
            self.api.shutdownServer()

    def calculateRefreshDelay(self):
        delay = int((self.last_fetch['refresh'] - ( time.mktime(time.localtime()) - self.last_fetch['time'] )) * 1000 + 100)
        if delay > 10100:
            delay = 10100
        if self.quit:
            delay = 100
        return delay

    def getUserInput(self):
        keyPressed = self.window.getUserInput()

        if self.debug:
            key_press = 'Captured key: ' + str(keyPressed)
            self.navigationController.displayKeyPress(key_press)

        return keyPressed