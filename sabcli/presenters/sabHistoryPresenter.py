import sys, curses

class sabHistoryPresenter( object ):
    def __init__(self):
        self.window = sys.modules["__main__"].window
        self.scroller = sys.modules["__main__"].scroller


    def displayUnpackStatus(self, item):
        if item.has_key("unpack_status"):
            self.window.pad.addStr('[unpack: ')
            if item["unpack_status"] > 0:
                self.window.pad.addStr('FAIL', curses.color_pair(2))
            else:
                self.window.pad.addStr('OK', curses.color_pair(3))
            self.window.pad.addStr(']')

    def displayRepairStatus(self, item):
        if item.has_key("repair_status"):
            self.window.pad.addStr('[par2: ')
            if item["repair_status"] > 0:
                self.window.pad.addStr('FAIL', curses.color_pair(2))
            else:
                self.window.pad.addStr('OK', curses.color_pair(3))
            self.window.pad.addStr(']')

    def displayRepairLog(self, item):
        if item.has_key("repair_log"):
            for log_item in item["repair_log"]:
                if log_item.find("Repair failed") > -1:
                    part1, part2 = log_item.split("Repair failed")
                    self.window.pad.addStr("       " + part1)
                    self.window.pad.addStr("Repair failed" + part2 + '\n', curses.color_pair(2))
                else:
                    self.window.pad.addStr("       " + log_item + '\n')

    def displayUnpackLog(self, item):
        if item.has_key("unpack_log"):
            for log_item in item["unpack_log"]:
                self.window.pad.addStr("       " + log_item + '\n')

    def displayDownloadInformation(self, index, item):
        if index < 10:
            self.window.pad.addStr(' ')
        self.window.pad.addStr('  ' + str(index), curses.color_pair(3))
        self.window.pad.addStr(' - ' + item["name"] + '\n')
        self.window.pad.addStr('       [download: ' + item['size'] + '] ')

    def display(self, state = {}):
        self.window.addString(2, 3, '# - Filename\n')
        self.window.addString(3, 0, '-' * int(self.window.size[1] + '\n'))

        for index, item in enumerate(state["history"]):

            self.displayDownloadInformation(index, item)

            self.displayRepairStatus(item)
            self.displayUnpackStatus(item)

            self.window.pad.addStr('\n')

            self.displayRepairLog(item)
            self.displayUnpackLog(item)

            self.window.pad.addStr('\n')

        self.scroller.display(state)