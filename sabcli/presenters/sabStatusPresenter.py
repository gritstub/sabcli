import  curses
import sys
import time

class sabStatusPresenter():

    def __init__(self):
        self.window = sys.modules["__main__"].window
        self.fetching = 'Fetching...'

    def display(self, state = {}):
        self.fetching = 'Fetching...' + (' ' * (len(state["disk_usage"]) - len('Fetching...')))
        self.display_diskwarnings(state)
        self.display_status(state)

    def display_diskwarnings(self, state = {}):
        if 'warning' in state:
            self.window.addString(1, 3, "WARNING:", curses.color_pair(2))
            self.window.addStr(state["warning"])

    def display_status(self, state = {}):
        status = self.printLine([state["disk_usage"], state["main_stats"], state["last_update"]])
        self.window.addString(int(self.window.size[0]) - 1, 0, status)

    def printLine(self, segments):
        # Calculate spacing between segments in line.
        space = int(self.window.size[1])
        ls = len(segments)

        for segment in segments:
            space -= len(segment)

        if ls > 1:
            space = space / (ls-1)

        if space <= 0:
            space = 1

        # Combine segments with equal spacing
        combined = ''
        for segment in segments:
            # Don't add segment if the combined line is wider than the screen
            if (len(combined) + len(segment) < int(self.window.size[1])):
                combined += segment + " " * space

            # Remove trailing whitespaces from above.
        return combined.strip()

    def display_fetching(self):
        self.window.addString(int(self.window.size[0])-1, 0, self.fetching)
        self.window.refresh()