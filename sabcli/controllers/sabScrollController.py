import sys
import curses

class sabScrollController( object ):

    def __init__(self):
        self.index = []
        self.view = 0

        self.scroll = {"totallines":0,
                       "firstline":0,
                       "lastline":0}

        self.window = sys.modules["__main__"].window

    def display(self):
        self.print_scroll()
