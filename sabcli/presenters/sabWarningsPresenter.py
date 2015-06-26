from cursesUI.cursesWindow import cursesWindow
from presenters.sabFlexibleScrollPresenter import sabFlexibleScrollPresenter


class sabWarningsPresenter():
    def __init__(self, window = None, flexibleScrollPresenter = None):
        if not window:
            window = cursesWindow()
        self.window = window

        if not flexibleScrollPresenter:
            flexibleScrollPresenter = sabFlexibleScrollPresenter()
        self.scrollPresenter = flexibleScrollPresenter

        self.screen = []
        self.pad = []

    def display(self, state):
        self.screen = []
        self.pad = []

        self.displayGeneralInformation()
        self.displayWarnings(state)

        self.window.draw(self.screen)
        self.window.pad.draw(self.pad)

        self.displayScrollAndItemSelection(state)

    def displayGeneralInformation(self):
        self.screen.append((3, 2, '[Date/Timestamp]          Type     | System message\n', ''))
        self.screen.append((0, 3, '-' * int(self.window.size[1] + '\n'), ''))

    def displayWarnings(self, state):
        for warning in state["warnings"]:
            warning["item_length"] = 1
            self.displayWarningInformation(warning)

    def displayScrollAndItemSelection(self, state):

        lengths = [item["item_length"] for item in state["warnings"]]
        state["item_lengths"] = lengths
        state["list_length"] = sum(lengths) + len(lengths)

        current_index = state["current_index"]
        if current_index < 0:
            current_index = 0

        before_start = [item["item_length"] for item in state["warnings"][:current_index]]
        state["selected_item_start"] = sum(before_start) + len(before_start)

        self.scrollPresenter.display(state)

    def displayWarningInformation(self, warning):
        self.pad.append(('   [' + warning["timestamp"] + '] ', ''))
        if warning["type"] == 'ERROR':
            self.pad.append((warning["type"], 2))
        else:
            self.pad.append((warning["type"], ''))

        warnings_length = len(warning["timestamp"]) + len(warning["type"])
        if warnings_length < 32:
            self.pad.append((" " * (32 - warnings_length), ''))
        self.pad.append(('|', ''))

        self.fitWarningMessageToWindow(warning)
        self.displayWarningMessage(warning)

    def fitWarningMessageToWindow(self, warning):
        message_padding = 39
        max_line_length = int(self.window.size[1]) - message_padding - 2

        temp = warning["message"].replace("&lt;", "<").replace("&gt;", ">").split(" ")

        lines = []
        line = ""
        for item in temp:
            if (len(item) + len(line) + 1) < max_line_length:
                line += item.strip() + " "
            else:
                lines.append(line)
                line = item + " "
        lines.append(line)

        warning["item_length"] = len(lines)
        warning["lines"] = lines

    def displayWarningMessage(self, warning):
        for index, line in enumerate(warning["lines"]):
            if index > 0:
                self.pad.append(('\n ' + " " * 36 + " |", ''))

            self.pad.append((' ' + line.strip(), ''))

        self.pad.append(('\n\n', ''))