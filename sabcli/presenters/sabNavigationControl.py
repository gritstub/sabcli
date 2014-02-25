import curses, sys

class sabNavigationControl():

    def __init__(self):
        self.window = sys.modules["__main__"].window

    def displaySpeed(self, state = {}):
        self.speed = "--"

        if state['paused'] == 'True':
            self.speed = "Paused"
        else:
            self.speed = "%.2f kb/s" %  float(state['kbpersec'])

        try:
            self.window.addString(0, int(self.window.size[1]) - 7 - len(self.speed), 'Speed: ')
        except:
            pass

        try:
            self.window.addString(0, int(self.window.size[1]) - len(self.speed), self.speed, curses.color_pair(7))
        except:
            pass

    def displayNavigation(self, selectedView):
        self.window.addString(0, 0, '')

        if selectedView in (0, 5):
            self.window.addStr('[1-Queue]', curses.color_pair(7))
        else:
            self.window.addStr('[1-Queue]')

        if selectedView == 1:
            self.window.addStr(' [2-History]', curses.color_pair(7))
        else:
            self.window.addStr(' [2-History]')

        if selectedView == 2:
            self.window.addStr(' [3-Warnings]', curses.color_pair(7))
        else:
            self.window.addStr(' [3-Warnings]')
        if selectedView == 3:
            self.window.addStr(' [4-More]', curses.color_pair(7))
        else:
            self.window.addStr(' [4-More]')
        if selectedView == 4:
            self.window.addStr(' [5-Help]', curses.color_pair(7))
        else:
            self.window.addStr(' [5-Help]')

    def display(self, selectedView = 0, speed = '--'):
        self.displayNavigation(selectedView)
        self.displaySpeed(speed)