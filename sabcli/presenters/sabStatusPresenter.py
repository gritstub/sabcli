import  curses
import sys
import time

class sabStatusControl():

    def __init__(self):
        self.window = sys.module["__main__"].window

    def display(self, state = {}):
        self.display_diskwarnings(state)
        self.display_status(state)

    def display_diskwarnings(self, state = {}):
        if float(state['mbleft']) / 1024 > float(state['diskspace2']):
            self.window.addString(1, 3, "WARNING:", curses.color_pair(2))
        self.window.addStr(" Insufficient free disk space left to finish queue.\n")
        if float(state['mbleft']) / 1024 > float(state['diskspacetotal2']):
            self.window.addString(1, 3, "WARNING:", curses.color_pair(2))
        self.window.addStr(" Insufficient total disk space to finish queue.\n")

    def display_status(self, state = {}):
        last_update = '[Updated: ' + time.strftime("%H:%M:%S", time.localtime(self.last_fetch['time'])) + '] '

        main_stats = ""
        if 'total_size' in state: # History view
            main_stats= str('[Transfered: %s / %s / %s]' % ( state['total_size'], state['month_size'], state['week_size']))
        else: # Queue view or pre 0.5.2 view
            main_stats = str('[Queue: %.2f / %.2f GB (%2.0f%%)] [Up: %s]' % (state["downloaded"], state["total_queue"], state["progress_pct"], state["uptime"]))

        disk_stats = '[Disk: %.2f / %.2f GB]' % ( float(rd['diskspace2']), float(rd['diskspacetotal2']))

        self.window.addString
        return self.printLine([disk_stats, main_stats, last_update])

    def printLine(self, segments):
    # Calculate spacing between segments in line.
        space = int(self.size[1])
        ls = len(segments)

        for segment in segments:
            space -= len(segment)

        if ls > 1:
            space = space / (ls-1)

        if space <= 0:
            space = 1

        # Combine segments with equal spacing
        combined = ''
        for segment in segments:
            # Don't add segment if the combined line is wider than the screen
            if (len(combined) + len(segment) < int(self.size[1])):
                combined += segment + " " * space

            # Remove trailing whitespaces from above.
        return combined.strip()

