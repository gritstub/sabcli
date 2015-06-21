from cursesUI.cursesWindow import cursesWindow


class sabHistoryPresenter:
    def __init__(self, window = None):
        if not window:
            window = cursesWindow()
        self.window = window

        self.screen = []
        self.pad = []

    def display(self, state):
        self.displayGeneralInformation()

        for index, item in enumerate(state["history"]):

            self.displayDownloadInformation(index, item)

            self.displayRepairStatus(item)
            self.displayUnpackStatus(item)

            self.window.pad.addStr('\n')

            self.displayRepairLog(item)
            self.displayUnpackLog(item)

            self.window.pad.addStr('\n')

        self.scroller.display(state)

    def displayGeneralInformation(self):
        self.window.addString(2, 3, '# - Filename\n', '')
        self.window.addString(3, 0, '-' * int(self.window.size[1] + '\n'), '')

    def displayDownloadInformation(self, index, item):
        self.pad.append(('  ' + str(index), 3))
        self.pad.append((' - ' + item["name"] + '\n', ''))
        self.pad.append(('       [size: ' + item['size'] + '] ', ''))

    def displayRepairStatus(self, item):
        if not item.has_key("repair_status"):
            return

        self.pad.append(('[par2: ', ''))
        if item["repair_status"] > 0:
            self.pad.append(('FAIL', 2))
        else:
            self.pad.append(('OK', 3))
        self.pad.append((']', ''))

    def displayUnpackStatus(self, item):
        if not item.has_key("unpack_status"):
            return

        self.pad.append(('[unpack: ', ''))
        if item["unpack_status"] > 0:
            self.pad.append(('FAIL', 2))
        else:
            self.pad.append(('OK', 3))
        self.pad.append((']', ''))

    def displayRepairLog(self, item):
        if not item.has_key("repair_log"):
            return

        for log_item in item["repair_log"]:
            if log_item.find("Repair failed") > -1:
                part1, part2 = log_item.split("Repair failed")
                self.pad.append(("       " + part1, ''))
                self.pad.append(("Repair failed" + part2 + '\n', 2))
            else:
                self.pad.append(("       " + log_item + '\n', ''))

    def displayUnpackLog(self, item):
        if not item.has_key("unpack_log"):
            return

        for log_item in item["unpack_log"]:
            self.pad.append(("       " + log_item + '\n', ''))