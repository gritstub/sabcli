import sys, time

class sabStatusController():

    def __init__(self):
        self.statusPresenter = sys.modules["__main__"].statusPresenter
        self.status = {}

    def updateWarnings(self, state):
        if float(state['mbleft']) / 1024 > float(state['diskspace2']):
            self.status["warning"] = " Insufficient free disk space left to finish queue.\n"
        if float(state['mbleft']) / 1024 > float(state['diskspacetotal2']):
            self.status["warning"] = " Insufficient total disk space to finish queue.\n"

    def updateStatistics(self, state):
        self.status["last_update"] = '[Updated: ' + time.strftime("%H:%M:%S", time.localtime(state['last_fetch_time'])) + '] '

        self.status["disk_usage"] = '[Disk: %.2f / %.2f GB]' % (float(state['diskspace2']), float(state['diskspacetotal2']))

        main_stats = ""
        if 'total_size' in state: # History view
            main_stats = str(
                '[Transfered: %s / %s / %s]' % ( state['total_size'], state['month_size'], state['week_size']))
        else: # Queue view or pre 0.5.2 view
            main_stats = str('[Queue: %.2f / %.2f GB (%2.0f%%)] [Up: %s]' % (
            state["downloaded"], state["total_queue"], state["progress_pct"], state["uptime"]))

        self.status["main_stats"] = main_stats

    def update(self, state = {}):
        if 'diskspace2' not in state and 'diskspacetotal2' not in state:
            return
        self.updateWarnings(state)
        self.updateStatistics(state)

    def display(self):
        self.statusPresenter.display(self.status)

    def display_fetching(self):
        self.statusPresenter.display_fetching()