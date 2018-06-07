import time


class sabDownloadQueueParser():

    def parse(self, response = {}):
        state = {'last_fetch_time': time.time(),
                 "status": response["queue"]["status"],
                 "speed": "%.2f kb/s" % float(response["queue"]["kbpersec"]),
                 "size_left": response["queue"]["sizeleft"],
                 "time_left": response["queue"]["timeleft"],
                 "mb": response["queue"]["mb"],
                 "mbleft": response["queue"]["mbleft"],
                 "diskspace2": response["queue"]["diskspace2"],
                 "diskspacetotal2": response["queue"]["diskspacetotal2"],
                 "downloaded": (float(response["queue"]['mb']) - float(response["queue"]['mbleft']) ) / 1024,
                 "total_queue": float(response["queue"]['mb']) / 1024,
                 "progress_pct": 100 * (float(response["queue"]['mb']) - float(response["queue"]['mbleft'])) / (float(response["queue"]['mb']) + 0.01)
        }

        state["queue"] = self.parseQueue(response)
        return state

    def parseQueue(self, response):
        slots = response["queue"]['slots']
        queue = []
        for slot in slots:
            timeleft = slot['timeleft']
            if len(slot['timeleft']) == 7:
                timeleft = "0" + timeleft

            item = {"filename": slot["filename"],
                    "index": slot["index"],
                    "avg_age": slot["avg_age"],
                    "priority": slot["priority"],
                    "unpackopts": int(slot["unpackopts"]),
                    "status": slot["status"],
                    "mb": slot["mb"],
                    "id": slot["nzo_id"],
                    "mb_left": slot["mbleft"],
                    "percentage": slot["percentage"],
                    "timeleft": timeleft
            }

            queue.append(item)
        return queue