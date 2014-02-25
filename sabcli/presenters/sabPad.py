import os, curses

class sabPad():

    def __init__(self):
        self.size = os.popen('stty size', 'r').read().split()
        self.pad = curses.newpad(10000, int(self.size[1])-2)

    def addStr(self, string, attr = ''):
        try:
            if not attr:
                self.pad.addstr(string)
            else:
                self.pad.addstr(string, attr)
        except:
            pass

    def addString(self, posY, posX, string, attr = ''):
        try:
            if not attr:
                self.pad.addstr(posY, posX, string)
            else:
                self.pad.addstr(posY, posX, string, attr)
        except:
            pass

    def refresh(self):
        self.update()

    def update(self):
        try:
            self.pad.noutrefresh(0, 0, 4, 0, int(self.size[0])-2, int(self.size[1])-2)
        except:
            pass

    def clear(self):
        self.pad.clear()