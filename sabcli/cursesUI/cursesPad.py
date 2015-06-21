import os
import curses


class cursesPad():
    def __init__(self):
        self.size = os.popen('stty size', 'r').read().split()
        self.pad = ''

    def initialize(self):
        self.pad = curses.newpad(10000, int(self.size[1]) - 2)

    def addStr(self, string, color = ''):
        try:
            if not color:
                self.pad.addstr(string)
            else:
                self.pad.addstr(string, curses.color_pair(color))
        except:
            pass

    def addString(self, posX, posY, string, color = ''):
        try:
            if not color:
                self.pad.addstr(posY, posX, string)
            else:
                self.pad.addstr(posY, posX, string, curses.color_pair(color))
        except:
            pass

    def refresh(self, line_number):
        try:
            self.pad.noutrefresh(line_number, 0, 4, 0, int(self.size[0]) - 2, int(self.size[1]) - 2)
        except:
            pass

    def draw(self, pad_instruction):
        if not pad_instruction:
            return

        if len(pad_instruction[0]) == 4:
            for (x, y, line, color) in pad_instruction:
                self.addString(x, y, line, color)
        elif len(pad_instruction[0]) == 2:
            for (line, color) in pad_instruction:
                self.addStr(line, color)

    def clear(self):
        self.pad.clear()