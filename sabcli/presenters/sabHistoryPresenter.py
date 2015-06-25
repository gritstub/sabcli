from cursesUI.cursesWindow import cursesWindow


class sabHistoryPresenter:
    def __init__(self, window = None):
        if not window:
            window = cursesWindow()
        self.window = window

        self.screen = []
        self.pad = []

    def display(self, state):
        self.screen = []
        self.pad = []

        self.displayGeneralInformation()
        self.displayHistory(state)

        self.window.draw(self.screen)
        self.window.pad.draw(self.pad)

    def displayGeneralInformation(self):
        self.screen.append((3, 2, '# - Filename\n', ''))
        self.screen.append((0, 3, '-' * int(self.window.size[1] + '\n'), ''))

    def displayHistory(self, state):
        for index, item in enumerate(state["history"]):
            self.displayDownloadInformation(index, item)

            self.displayRepairStatus(item)
            self.displayUnpackStatus(item)

            self.pad.append(('\n', ''))

            self.displayRepairLog(item)
            self.displayUnpackLog(item)

            self.pad.append(('\n', ''))

    def displayDownloadInformation(self, index, item):
        self.pad.append(('  ' + str(index), 3))
        self.pad.append((' - ' + item["name"] + '\n', ''))
        self.pad.append(('       [size: ' + item['size'] + '] ', ''))

    def displayRepairStatus(self, item):
        if "repair_status" not in item:
            return

        self.pad.append(('[par2: ', ''))
        if item["repair_status"] > 0:
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

        item["length"] = length

    def displayUnpackLog(self, item):
        if "unpack_log" not in item:
            return

        length = item.get("item_length", 0)

        for log_item in item["unpack_log"]:
            self.pad.append(("       " + log_item + '\n', ''))
            length += 1

        item["length"] = length