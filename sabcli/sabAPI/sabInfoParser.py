import traceback

class sabInfoParser():

    def parse(self, response):
        state = {
                 "cpumodel": response["status"]["cpumodel"],
                 "diskspace1": response["status"]["diskspace1"],
                 "diskspace2": response["status"]["diskspace2"],
                 "diskspacetotal1": response["status"]["diskspacetotal1"],
                 "diskspacetotal2": response["status"]["diskspacetotal2"],
                 "loadavg": response["status"]["loadavg"],
                 "speedlimit": response["status"]["speedlimit_abs"],
                 "uptime": response["status"]["uptime"],
                 "version": response["status"]["version"]
        }

        if state["speedlimit"] == "":
            state["speedlimit"] = "None"

        return state
