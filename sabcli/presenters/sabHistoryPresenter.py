from cursesUI.cursesWindow import cursesWindow
from presenters.sabFlexibleScrollPresenter import sabFlexibleScrollPresenter


class sabHistoryPresenter:
    def __init__(self, window = None, scrollPresenter = None):
        if not window:
            window = cursesWindow()
        self.window = window

        if not scrollPresenter:
            scrollPresenter = sabFlexibleScrollPresenter()
        self.scrollPresenter = scrollPresenter

        self.screen = []
        self.pad = []

    def display(self, state):
        self.screen = []
        self.pad = []

        self.displayGeneralInformation()
        self.displayHistory(state)

        self.window.draw(self.screen)
        self.window.pad.draw(self.pad)

        self.displayScrollAndItemSelection(state)

    def displayGeneralInformation(self):
        self.screen.append((3, 2, '# - Filename\n', ''))
        self.screen.append((0, 3, '-' * int(self.window.size[1] + '\n'), ''))

    def displayHistory(self, state):
        for index, item in enumerate(state["history"]):
            item["item_length"] = 2
            self.displayDownloadInformation(index, item)

            self.displayRepairStatus(item)
            self.displayUnpackStatus(item)

            self.pad.append(('\n', ''))

            self.displayRepairLog(item)
            self.displayUnpackLog(item)

            self.pad.append(('\n', ''))

    def displayScrollAndItemSelection(self, state):
        lengths = [item["item_length"] for item in state["history"]]
        state["item_lengths"] = lengths
        state["list_length"] = sum(lengths) + len(lengths)

        current_index = state["current_index"]
        if current_index < 0:
            current_index = 0

        before_start = [item["item_length"] for item in state["history"][:current_index]]
        state["selected_item_start"] = sum(before_start) + len(before_start)

        self.scrollPresenter.display(state)

    def displayDownloadInformation(self, index, item):
        self.pad.append(('   ' + str(index), 3))
        self.pad.append((' - ' + item["name"] + '\n', ''))
        self.pad.append(('       [size: ' + item['size'] + '] ', ''))

    def displayRepairStatus(self, item):
        if "repair_status" not in item:
            return

        self.pad.append(('[par2: ', ''))
        if item["repair_status"] == 1:
            self.pad.append(('NONE', 6))
        elif item["repair_status"] > 1:
            self.pad.append(('FAIL', 2))
        else:
            self.pad.append(('OK', 3))
        self.pad.append((']', ''))

    def displayUnpackStatus(self, item):
        if "unpack_status" not in item:
            return

        self.pad.append(('[unpack: ', ''))
        if item["unpack_status"] > 0:
            self.pad.append(('FAIL', 2))
        else:
            self.pad.append(('OK', 3))
        self.pad.append((']', ''))

    def displayRepairLog(self, item):
        if "repair_log" not in item:
            return

        length = item.get("item_length", 0)

        for log_item in item["repair_log"]:
            if log_item.find("Repair failed") > -1:
                part1, part2 = log_item.split("Repair failed")
                self.pad.append(("       " + part1, ''))
                self.pad.append(("Repair failed" + part2 + '\n', 2))
            else:
                self.pad.append(("       " + log_item + '\n', ''))
            length += 1

        item["item_length"] = length

    def displayUnpackLog(self, item):
        if "unpack_log" not in item:
            return

        length = item.get("item_length", 0)

        for log_item in item["unpack_log"]:
            self.pad.append(("       " + log_item + '\n', ''))
            length += 1

        item["item_length"] = length