from cursesUI.cursesWindow import cursesWindow
from presenters.sabScrollPresenter import sabScrollPresenter


class sabQueuePresenter():
    def __init__(self, window = None, scrollPresenter = None):
        if not window:
            window = cursesWindow()
        self.window = window

        if not scrollPresenter:
            scrollPresenter = sabScrollPresenter()
        self.scrollPresenter = scrollPresenter

        self.options = ["Download", "Repair", "Unpack", "Delete"]

        self.screen = []
        self.pad = []

    def display(self, state):
        self.screen = []
        self.pad = []

        self.displayGeneralInformation()
        self.displayQueue(state)

        self.window.draw(self.screen)
        self.window.pad.draw(self.pad)

        state["item_size"] = 3
        self.scrollPresenter.display(state)

    def displayGeneralInformation(self):
        self.screen.append((3, 2, "# - Filename [Age/Priority/Options] (Status):\n", ""))
        self.screen.append((0, 3, "-" * int(self.window.size[1] + "\n"), ""))

    def displayQueue(self, state = {}):
        padding = self.calculateProgressBarPadding(state)

        for slot in state["queue"]:
            if slot["index"] == state["current_index"]:
                self.displayFileInformation(slot, state["current_selection"])
            else:
                self.displayFileInformation(slot)
            self.displayProgress(padding, slot)

    def calculateProgressBarPadding(self, state):
        doubleMaxTailLength = 0
        for slot in state["queue"]:
            if doubleMaxTailLength < len(slot["mb"]):
                doubleMaxTailLength = len(slot["mb"])
        doubleMaxTailLength += doubleMaxTailLength
        return doubleMaxTailLength

    def displayFileInformation(self, slot, current_selection = -1):
        self.pad.append((' ' * (4 - len(str(slot["index"]))), ''))
        self.pad.append((str(slot['index']), 3))
        self.pad.append((" - ", ""))
        if current_selection == 0:
            self.pad.append((slot["filename"], 2))
        else:
            self.pad.append((slot["filename"], ""))

        self.pad.append((' [', ''))
        self.pad.append((slot['avg_age'], 3))
        self.pad.append(('/', ''))

        if current_selection == 1:
            self.pad.append((slot['priority'], 2))
        else:
            self.pad.append((slot['priority'], 3))
        self.pad.append(('/', ''))

        if current_selection == 2:
            self.pad.append((self.options[int(slot['unpackopts'])], 2))
        else:
            self.pad.append((self.options[int(slot['unpackopts'])], 3))

        self.pad.append(('] (', ''))
        self.pad.append((slot['status'], 2))
        self.pad.append((')\n', ''))

    def displayProgress(self, alignment_length, slot):
        self.pad.append(('      ', ''))
        self.pad.append((slot["timeleft"], 2))
        self.pad.append((' ', ''))

        tail = "%.2f / %.2f [%2.0f%%]" % (float(slot['mb']) - float(slot['mb_left']), float(slot['mb']), float(slot['percentage']))
        tailLength = len(tail)
        charsLeft = int(self.window.size[1]) - len(slot["timeleft"]) - tailLength - 9 - (alignment_length + 9 - tailLength) - 5
        pct = charsLeft / 100.0 * float(slot['percentage'])
        progress = "=" * int(pct) + ">" + " " * (charsLeft - int(pct))

        self.pad.append(('[' + progress + ']', 5))
        self.pad.append((' ' * (alignment_length + 10 - tailLength), ''))
        self.pad.append(("%.2f" % (float(slot['mb']) - float(slot['mb_left'])), 2))
        self.pad.append((' / ', ''))
        self.pad.append(("%.2f" % (float(slot['mb'])), 2))
        self.pad.append((' [', ''))
        self.pad.append(("%2.0f%%" % (float(slot['percentage'])), 2))
        self.pad.append((']\n\n', ''))

    def wait(self, delay):
        self.window.wait(delay)

    def editDownloadName(self, selected_index, state):

        line_pad_index = selected_index * state["item_size"]
        pad_start_line = self.scrollPresenter.calculateScrollingLine(state)
        line_index = line_pad_index - pad_start_line + 4
        name = state["queue"][selected_index]["filename"]

        return self.window.editTextOnScreen(line_index, name)