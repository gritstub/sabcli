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

        elif keyPressed == 260 and not self.currentController.selected: # Curser left
            i = self.controllers.index(self.currentController)
            if i == 0:
                i = len(self.controllers) - 1
            else:
                i = i - 1
            self.currentController = self.controllers[i]

        elif keyPressed == 261 and not self.currentController.selected: # Curser right
            i = self.controllers.index(self.currentController)
            if i == len(self.controllers) - 1:
                i = 0
            else:
                i = i + 1
            self.currentController = self.controllers[i]

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

        elif keyPressed == ord('P') and not self.currentController.selected:
            self.action = 7 # pause

        #elif keyPressed == ord('S'): self.action = 7 # shutdown
        #elif keyPressed == ord('R'): self.action = 8 # restart

        elif keyPressed == 258 and not self.currentController.selected: # Curser down
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
            self.window.addString(1, int(self.window.size[1]) - len(key_press), key_press)
            self.window.refresh()

        return keyPressed

    def display(self):
        self.window.clear()
        self.window.addString(0, 0, '')
        self.window.addString(1, 50, 'controller: ' + str(self.controllers.index(self.currentController)))
        self.navigation.update(self.controllers.index(self.currentController), self.state)
        self.navigation.display()
        self.currentController.display()
        self.status.update(self.state)
        self.status.display()
        self.window.update()

    def run(self):

        while self.quit == 0:
            self.state = self.currentController.update()

            self.display()

            delay = self.calculateRefreshDelay()
            self.window.wait(delay)
            keyPressed = self.getUserInput()

            if self.currentController.selected:
                if not self.currentController.handleInput(keyPressed):
                    self.handleInput(keyPressed)
            else:
                self.handleInput(keyPressed)
        self.window.close()