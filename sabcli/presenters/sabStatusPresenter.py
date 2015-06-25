from cursesUI.cursesWindow import cursesWindow


class sabStatusPresenter():
    def __init__(self, window = None):
        if not window:
            window = cursesWindow()
        self.window = window
        self.fetching = 'Fetching...'

        self.screen = []
        self.pad = []

    def display(self, state):
        self.screen = []
        self.pad = []

        self.displayDiskWarning(state)
        self.displayGeneralStatus(state)

        self.window.draw(self.screen)
        self.window.pad.draw(self.pad)

    def displayDiskWarning(self, state):
        if 'warning' in state:
            self.screen.append((3, 1, "WARNING: " + state["warning"], 2))

    def displayGeneralStatus(self, state):
        status = self.printLine([state["disk_usage"], state["main_stats"], state["last_update"]])
        self.fetching = 'Fetching...' + (' ' * (len(state["disk_usage"]) - len('Fetching...')))
        self.screen.append((0, int(self.window.size[0]) - 1, status, ''))

    def printLine(self, segments):
        # Calculate spacing between segments in line.
        space = int(self.window.size[1])
        ls = len(segments)

        for segment in segments:
            space -= len(segment)

        if ls > 1:
            space = space / (ls - 1)

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

    def displayFetching(self):
        self.screen = []
        self.screen.append((0, int(self.window.size[0]) - 1, self.fetching, ''))
        self.window.draw(self.screen)
        self.window.refresh()