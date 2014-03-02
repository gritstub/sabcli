import sys, time

class sabController():

    def __init__(self):
        self.api = sys.modules["__main__"].api
        self.window = sys.modules["__main__"].window
        self.settings = sys.modules["__main__"].settings

        #internal members
        self.last_fetch = {'fetch': '', 'refresh': 10, 'time': time.mktime(time.localtime())}
        self.state = {}
        self.debug = True
        self.quit = 0

        #presenters
        self.navigation = sys.modules["__main__"].navigationController
        self.status = sys.modules["__main__"].statusController

        #controllers
        self.currentController = sys.modules["__main__"].queueController
        self.controllers = [sys.modules["__main__"].queueController, sys.modules["__main__"].historyController, sys.modules["__main__"].warningsController, sys.modules["__main__"].miscController, sys.modules["__main__"].helpController]

    def handleInput(self, keyPressed):
        self.window.addStr('handling keypress: ' + repr(keyPressed))

        if keyPressed == ord('Q') or keyPressed == ord('q'): # quit
            self.quit = 1

        elif keyPressed == 260: # Curser left
            current_controller_index = self.controllers.index(self.currentController)
            if current_controller_index > 0:
                current_controller_index -= 1
            else:
                current_controller_index = len(self.controllers) - 1

            self.currentController = self.controllers[current_controller_index]

        elif keyPressed == 261: # Curser right
            current_controller_index = self.controllers.index(self.currentController)
            if current_controller_index < len(self.controllers) - 1:
                current_controller_index += 1
            else:
                current_controller_index = 0

            self.currentController = self.controllers[current_controller_index]

        elif keyPressed == ord('1'): # queue
            self.currentController = self.controllers[0]
        elif keyPressed == ord('2'): # history
            self.currentController = self.controllers[1]
        elif keyPressed == ord('3'): # warnings
            self.currentController = self.controllers[2]
        elif keyPressed == ord('4'): # more
            self.currentController = self.controllers[3]
        elif keyPressed == ord('5') or keyPressed == ord('?'): # help
            self.currentController = self.controllers[4]

        elif keyPressed == ord('p'): # pause
            self.api.pauseServer()
        elif keyPressed == ord('r'): # resume
            self.api.resumeServer()
        elif keyPressed == ord('S'): # shutdown
            self.api.shutdownServer()
        elif keyPressed == 258: # Curser down
            self.currentController.selected = True
        elif keyPressed == 259: # Curser up
            self.currentController.selected = True

    def calculateRefreshDelay(self):
        delay = int((self.last_fetch['refresh'] - ( time.mktime(time.localtime()) - self.last_fetch['time'] )) * 1000 + 100)
        if delay > 10100:
            delay = 10100
        if self.quit:
            delay = 100;
        return delay

    def getUserInput(self):
        keyPressed = self.window.getUserInput()

        if self.debug:
            key_press = 'Captured key: ' + str(keyPressed)
            self.navigation.displayKeyPress(key_press)

        return keyPressed

    def display(self):
        self.window.clear()
        self.navigation.display()
        self.currentController.display()
        self.status.display()
        self.window.update()

    def updateApplicationState(self):
        self.state = self.currentController.update()
        self.navigation.update(self.controllers.index(self.currentController), self.state)
        self.status.update(self.state)

    def handleUserEvents(self):
        keyPressed = self.getUserInput()
        if not self.currentController.selected:
            self.handleInput(keyPressed)

        if self.currentController.selected:
            if not self.currentController.handleInput(keyPressed):
                self.handleInput(keyPressed)

    def waitForRefresh(self):
        delay = self.calculateRefreshDelay()
        self.window.wait(delay)

    def run(self):

        while self.quit == 0:
            self.updateApplicationState()

            self.display()

            self.waitForRefresh()

            self.handleUserEvents()

        self.window.close()