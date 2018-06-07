import datetime

class sabWarningsParser():

    def parse(self, response):
        state = {}
        state["warnings"] = self.parseWarnings(response["warnings"])

        return state

    def parseWarnings(self, warnings):
        log = []

        for warning in warnings:
            entry = {
                "timestamp": datetime.datetime.fromtimestamp(warning["time"]).strftime('%Y-%m-%d %H:%M:%S'),
                "type": warning["type"],
                "message": warning["text"]
            }
            log.append(entry)

        return log
