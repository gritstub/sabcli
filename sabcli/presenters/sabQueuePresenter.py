import sys
import curses

class sabQueuePresenter( object ):
    def __init__(self):
        self.window = sys.modules["__main__"].window
        self.scroller = sys.modules["__main__"].scroller
        self.options = ['Download', 'Repair', 'Unpack', 'Delete']

    def wait(self, delay):
        self.window.wait(delay)

    def display(self, state = {}):
        self.displayQueue(state)
        self.scroller.display()

    def displayFileInformation(self, slot, current_selection = -1):
        self.window.pad.addStr('   ' + str(slot['index']), curses.color_pair(3))
        self.window.pad.addStr(' - ')
        if current_selection == 0:
            self.window.pad.addStr(slot['filename'], curses.color_pair(2))
        else:
            self.window.pad.addStr(slot['filename'])

        self.window.pad.addStr(' [')
        self.window.pad.addStr(slot['avg_age'], curses.color_pair(3))
        self.window.pad.addStr('/')

        if current_selection == 1:
            self.window.pad.addStr(slot['priority'], curses.color_pair(2))
        else:
            self.window.pad.addStr(slot['priority'], curses.color_pair(3))
        self.window.pad.addStr('/')

        if current_selection == 2:
            self.window.pad.addStr(self.options[int(slot['unpackopts'])], curses.color_pair(2))
        else:
            self.window.pad.addStr(self.options[int(slot['unpackopts'])], curses.color_pair(3))

        self.window.pad.addStr('] (')
        self.window.pad.addStr(slot['status'], curses.color_pair(2))
        self.window.pad.addStr(')\n')

    def calculateProgressBarPadding(self, state):
        doubleMaxTailLength = 0
        for slot in state["queue"]:
            if doubleMaxTailLength < len(slot['mb']):
                doubleMaxTailLength = len(slot['mb'])
        doubleMaxTailLength += doubleMaxTailLength
        return doubleMaxTailLength

    def displayProgress(self, alignementLength, slot):
        self.window.pad.addStr('      ')
        self.window.pad.addStr(slot["timeleft"], curses.color_pair(2))
        self.window.pad.addStr(' ')
        tail = "%.2f / %.2f [%2.0f%%]" % (float(slot['mb']) - float(slot['mb_left']), float(slot['mb']), float(slot['percentage']) )
        tailLength = len(tail)
        charsLeft = int(self.window.size[1]) - len(slot["timeleft"]) - tailLength - 9 - (alignementLength + 9 - tailLength) - 5
        pct = (charsLeft) / 100.0 * float(slot['percentage'])
        progress = "=" * int(pct) + ">" + " " * (charsLeft - int(pct))
        self.window.pad.addStr('[' + progress + ']', curses.color_pair(5) | curses.A_BOLD) #
        self.window.pad.addStr(' ' * ( alignementLength + 10 - tailLength))
        self.window.pad.addStr("%.2f" % (float(slot['mb']) - float(slot['mb_left'])), curses.color_pair(2))
        self.window.pad.addStr(' / ')
        self.window.pad.addStr("%.2f" % (float(slot['mb'])), curses.color_pair(2))
        self.window.pad.addStr(' [')
        self.window.pad.addStr("%2.0f%%" % (float(slot['percentage'])), curses.color_pair(2))
        self.window.pad.addStr(']\n\n')

    def displayQueue(self, state = {}):
        self.window.addString(2, 3, '# - Filename [Age/Priority/Options] (Status):\n')
        self.window.addString(3, 0, '-' * int(self.window.size[1] + '\n'))

        padding = self.calculateProgressBarPadding(state)

        for slot in state["queue"]:
            if slot["index"] == state["current_index"]:
                self.displayFileInformation(slot, state["current_selection"])
            else:
                self.displayFileInformation(slot)
            self.displayProgress(padding, slot)
        
        self.displaySelectedItem(state)
        self.scrollViewPort(state)

    def displaySelectedItem(self, state):
        if state["current_index"] > -1:
            start = state["current_index"] * 3
            for i in [0 , 1]:
                self.window.pad.addString(i + start, 0, '*')

    def scrollViewPort(self, state):
        #self.window.pad.scrollToLine()
        pass

