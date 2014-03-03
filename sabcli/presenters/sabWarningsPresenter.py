import curses
import sys

class sabWarningsPresenter( object ):
    def __init__(self):
        self.window = sys.modules["__main__"].window
        self.scroller = sys.modules["__main__"].scroller

    def display_warning(self, warning):
        self.window.pad.addStr('   [' + warning["timestamp"] + '] ')
        if warning["type"] == 'ERROR':
            self.window.pad.addStr(warning["type"], curses.color_pair(2))
        else:
            self.window.pad.addStr(warning["type"])
        warnings_length = len(warning["timestamp"]) + len(warning["type"])
        if warnings_length < 32:
            self.window.pad.addStr(" " * (32 - warnings_length))
        self.window.pad.addStr('|')
        self.window.pad.addStr(' ' + warning["message"] + '\n\n')

    def display_header(self):
        self.window.addString(2, 3, '[Date/Timestamp         ] Type     | System message\n')
        self.window.addString(3, 0, '-' * int(self.window.size[1] + '\n'))

    def display(self, state = {}):
        self.display_header()

        for warning in state["warnings"]:
            self.display_warning(warning)

        self.scroller.display(state)