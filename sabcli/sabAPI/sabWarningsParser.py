class sabWarningsParser():

    def parse(self, response = {}):

        state = {}

        warnings = []
        if response["warnings"] != None:
            try:
                response["warnings"].keys()
                warnings = [ response["warnings"]['warning'] ]
            except AttributeError:
                warnings = response["warnings"]['warning']

            if warnings[0][0] != 1:
                warnings = warnings[0]
            if type(warnings) == str or type(warnings) == unicode:
                warnings = [warnings]

        log = []
        for warning in warnings:
            warning = warning.split("\n")
            warning[2] = warning[2].replace("WARNING: ","")
            if warning[2].find(':') > 0:
                warning[2] = warning[2][:warning[2].find(':')]
            entry = {
                "timestamp" : warning[0],
                "type": warning[1],
                "message": warning[2]
            }
            log.append(entry)
        state["warnings"] = log
        return state