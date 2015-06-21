from cursesUI.cursesWindow import cursesWindow


class sabWarningsPresenter():
    def __init__(self, window = None):
        if not window:
            window = cursesWindow()
        self.window = window

        self.screen = []
        self.pad = []

    def display(self, state = {}):
        self.screen = []
        self.pad = []

        self.displayGeneralInformation()

        for warning in state["warnings"]:
            self.displayWarningInformation(warning)

        self.window.draw(self.screen)
        self.window.pad.draw(self.pad)

    def displayGeneralInformation(self):
        self.screen.append((3, 2, '[Date/Timestamp]          Type     | System message\n', ''))
        self.screen.append((0, 3, '-' * int(self.window.size[1] + '\n'), ''))

    def displayWarningInformation(self, warning):
        self.pad.append(('   [' + warning["timestamp"] + '] ', ''))
        if warning["type"] == 'ERROR':
            self.pad.append((warning["type"], 2))
        else:
            self.pad.append((warning["type"]), '')

        warnings_length = len(warning["timestamp"]) + len(warning["type"])
        if warnings_length < 32:
            self.pad.append((" " * (32 - warnings_length), ''))

        self.pad.append(('|', ''))
        self.pad.append((' ' + warning["message"] + '\n\n', ''))