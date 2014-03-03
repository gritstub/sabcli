import time
class sabHistoryParser():

    def extractStageLog(self, slot):
        actions = slot["stage_log"]
        return actions

    def extractUnpackOperationStatus(self, action, item):
        unpack_log = []
        unpack_fail = 0
        for error_string in action['actions']:
            if error_string.find('Unpacked') < 0:
                unpack_log.append(error_string)
                unpack_fail = 1

        item["unpack_fail"] = unpack_fail
        item["unpack_log"] = unpack_log

    def parseHistory(self, response):
        slots = response["history"]['slots']

        history = []
        for slot in slots:
            item = {"index": slot["id"] - 1,
                    "name": slot["name"],
                    "size": slot["size"],
                    "id":slot["nzo_id"],
                    "status": slot["status"],
            }

            stage_log = self.extractStageLog(slot)

            for action in stage_log:
                if action['name'] == "Unpack":
                    self.extractUnpackOperationStatus(action, item)

                if action['name'] == "Repair":
                    self.extractRepairOperationStatus(action, item)

            history.append(item)
        history.reverse()
        return history

    def parse(self, response = {}):
        state = {'last_fetch_time':time.time(),
                 "status":response["history"]["status"],
                 "speed":"%.2f kb/s" % float(response["history"]["kbpersec"]),
                 "size_left":response["history"]["sizeleft"],
                 "time_left":response["history"]["timeleft"],
                 "mb":response["history"]["mb"],
                 "mbleft":response["history"]["mbleft"],
                 "diskspace2":response["history"]["diskspace2"],
                 "diskspacetotal2":response["history"]["diskspacetotal2"],
                 "total_size":response["history"]["total_size"],
                 "month_size":response["history"]["month_size"],
                 "week_size":response["history"]["week_size"]
        }

        state["history"] = self.parseHistory(response)
        return state

    def extractRepairOperationStatus(self, action, item):
        repair_log = []
        repair_fail= 0
        for error_string in action['actions']:
            if error_string.find('Quick Check OK') < 0 and error_string.find('Repaired in') < 0 and error_string.find('all files correct') < 0:
                repair_log.append(error_string)
                repair_fail= 1

        item["repair_status"] = repair_fail
        item["repair_log"] = repair_log