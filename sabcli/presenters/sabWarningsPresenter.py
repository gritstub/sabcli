import curses
import sys

class sabWarningsPresenter( object ):
    def __init__(self):
        self.window = sys.modules["__main__"].window

    def display(self, state = {}):
        self.window.addString(2, 3, '[Date/Timestamp         ] Type     | System message\n')
        self.window.addString(3, 0, '-' * int(self.window.size[1] + '\n'))

        for warning in state["warnings"]:
            self.window.pad.addStr('   [' + warning["timestamp"] + '] ')

            if warning["type"] == 'ERROR':
                self.window.pad.addStr(warning["type"], curses.color_pair(2))
            else:
                self.window.pad.addStr(warning["type"])
            warnings_length = len(warning["timestamp"]) + len(warning["type"])

            if warnings_length < 32:
                self.window.pad.addStr(" " * (32-warnings_length))
            self.window.pad.addStr('|')
            self.window.pad.addStr(' ' + warning["message"] + '\n\n')

        self.window.pad.addStr('\n\n')