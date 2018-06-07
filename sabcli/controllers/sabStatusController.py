import time
from presenters.sabStatusPresenter import sabStatusPresenter
import sabAPI


class sabStatusController():
    def __init__(self, api = None, statusPresenter = None):
        if not api:
            api = sabAPI.api.api()
        self.api = api

        if not statusPresenter:
            statusPresenter = sabStatusPresenter()
        self.statusPresenter = statusPresenter

        self.status = {}

    def updateWarnings(self, state):
        if float(state["mbleft"]) / 1024 > float(state["diskspace2"]):
            self.status["warning"] = " Insufficient free disk space left to finish queue.\n"
        if float(state["mbleft"]) / 1024 > float(state["diskspacetotal2"]):
            self.status["warning"] = " Insufficient total disk space to finish queue.\n"

    def updateStatistics(self, state, fullStatus):
        self.status["disk_usage"] = str("[Disk: %.2f / %.2f GB] [Up: %s]" %
                                        (float(fullStatus["diskspace2"]), float(fullStatus["diskspacetotal2"]), fullStatus["uptime"]))
        if "last_fetch_time" in state:
            self.status["last_update"] = "[Updated: " + time.strftime("%H:%M:%S", time.localtime(state["last_fetch_time"])) + "] "
        else:
            self.status["last_update"] = ""

        main_stats = ""
        if "total_size" in state:  # History view
            main_stats = str("[Transfered: %s total / %s month / %s week]" %
                             (state['total_size'], state['month_size'], state['week_size']))
        elif "downloaded" in state:  # Queue view
            main_stats = str("[Queue: %.2f / %.2f GB (%2.0f%%)]" %
                             (state["downloaded"], state["total_queue"], state["progress_pct"]))
        else:
            main_stats = str("[CPU: %s]" %
                             (fullStatus["cpumodel"]))

        self.status["main_stats"] = main_stats

    def update(self, state):
        fullStatus = self.api.getApiInfo()
        if "mbleft" in state:
            self.updateWarnings(state)
        self.updateStatistics(state, fullStatus)

    def display(self):
        self.statusPresenter.display(self.status)

    def displayFetching(self):
        self.statusPresenter.displayFetching()