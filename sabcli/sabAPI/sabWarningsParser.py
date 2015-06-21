class sabWarningsParser():

    def parse(self, response):
        state = {}
        state["warnings"] = self.parseWarnings(response["warnings"])

        return state

    def parseWarnings(self, warnings):
        log = []

        for warning in warnings:
            warning = warning.split("\n")
            warning[2] = warning[2].replace("WARNING: ", "")
            warning[2] = warning[2].replace("filename=", "")
            warning[2] = warning[2].replace(", type=None", "")
            entry = {
                "timestamp": warning[0],
                "type": warning[1],
                "message": warning[2]
            }
            log.append(entry)

        return log
