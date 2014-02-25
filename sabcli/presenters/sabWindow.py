import os, curses
import signal
from presenters.sabPad import sabPad

class sabWindow():

    def __init__(self):
        self.stdscr = self.initialise_window()
        self.initialise_color_pairs()

        self.size = os.popen('stty size', 'r').read().split()
        self.win = curses.newwin(int(self.size[0]), int(self.size[1]), 0, 0)
        self.pad = sabPad()
        signal.signal(signal.SIGWINCH, self.sigwinch_handler)

    # Private Methods
    def sigwinch_handler(self, n, frame):
        self.size = os.popen('stty size', 'r').read().split()

    def getUserInput(self):
        return self.stdscr.getch()

    def setCursorVisibility(self, visible = 0):
        try:
            curses.curs_set(visible)
        except:
            pass

    def initialise_window(self):
        screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.noecho()
        curses.cbreak()

        screen.keypad(1)
        self.setCursorVisibility(0)
        return screen

    def initialise_color_pairs(self):
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        curses.init_pair(4, curses.COLOR_YELLOW, -1)
        curses.init_pair(5, curses.COLOR_BLUE, -1)
        curses.init_pair(6, curses.COLOR_MAGENTA, -1)
        curses.init_pair(7, curses.COLOR_CYAN, -1)
        curses.init_pair(8, curses.COLOR_WHITE, -1)

    def close(self):
        self.setCursorVisibility(1)
        curses.nocbreak();
        self.stdscr.keypad(0);
        curses.echo()
        curses.endwin()

    def getInput(self, edit_window):
        self.setCursorVisibility(1)
        value = curses.textpad.Textbox(edit_window, insert_mode = True).edit().strip()
        self.setCursorVisibility(0)
        return value

    def wait(self, delay):
        self.stdscr.timeout(delay)

    def addStr(self, string, attr = ''):
        try:
            if not attr:
                self.stdscr.addstr(string)
            else:
                self.stdscr.addstr(string, attr)
        except:
            pass

    def addString(self, posY, posX, string, attr = ''):
        try:
            if not attr:
                self.stdscr.addstr(posY, posX, string)
            else:
                self.stdscr.addstr(posY, posX, string, attr)
        except:
            pass

    def refresh(self):
        self.stdscr.refresh()
        self.pad.refresh()
        curses.doupdate()

    def update(self):
        self.stdscr.noutrefresh()
        self.pad.update()
        curses.doupdate()

    def clear(self):
        self.stdscr.clear()
        self.pad.clear()