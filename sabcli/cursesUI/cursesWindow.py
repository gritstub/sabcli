import os
import curses
import signal
from cursesUI.cursesPad import cursesPad


class cursesWindow():
    __shared_state = {}

    def __init__(self, pad = None):
        self.__dict__ = self.__shared_state

        if not pad:
            pad = cursesPad()
        self.pad = pad

        self.screen = ''
        self.window = ''
        self.size = os.popen('stty size', 'r').read().split()

    def initialize(self):
        self.initializeWindow()
        self.initializeColorScheme()

    def initializeWindow(self):
        self.screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(1)
        self.setCursorVisibility(0)
        self.window = curses.newwin(int(self.size[0]), int(self.size[1]), 0, 0)
        signal.signal(signal.SIGWINCH, self.windowSizeChangeEventHandler)

    def initializeColorScheme(self):
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        curses.init_pair(4, curses.COLOR_YELLOW, -1)
        curses.init_pair(5, curses.COLOR_BLUE, -1)
        curses.init_pair(6, curses.COLOR_MAGENTA, -1)
        curses.init_pair(7, curses.COLOR_CYAN, -1)
        curses.init_pair(8, curses.COLOR_WHITE, -1)

    def windowSizeChangeEventHandler(self, n, frame):
        self.size = os.popen('stty size', 'r').read().split()

    def setCursorVisibility(self, visible = 0):
        try:
            curses.curs_set(visible)
        except:
            pass

    def getUserInput(self):
        return self.screen.getch()

    def close(self):
        self.setCursorVisibility(1)
        curses.nocbreak()
        self.screen.keypad(0)
        curses.echo()
        curses.endwin()

    def getInput(self, edit_window):
        self.setCursorVisibility(1)
        value = curses.textpad.Textbox(edit_window, insert_mode = True).edit().strip()
        self.setCursorVisibility(0)
        return value

    def wait(self, delay):
        self.screen.timeout(delay)

    def refresh(self):
        try:
            self.screen.noutrefresh()
        except:
            pass

    def update(self):
        curses.doupdate()

    def clear(self):
        self.screen.clear()
        self.pad.clear()

    # Drawing
    def addStr(self, string, color = ''):
        try:
            if not color:
                self.screen.addstr(string)
            else:
                self.screen.addstr(string, curses.color_pair(color))
        except:
            pass

    def addString(self, posX, posY, string, color = ''):
        try:
            if not color:
                self.screen.addstr(posY, posX, string)
            else:
                self.screen.addstr(posY, posX, string, curses.color_pair(color))
        except:
            pass

    def draw(self, screen):
        if not screen:
            return

        if len(screen[0]) == 4:
            for (y, x, line, color) in screen:
                self.addString(y, x, line, color)
        elif len(screen[0]) == 2:
            for (line, color) in screen:
                self.addStr(line, color)
