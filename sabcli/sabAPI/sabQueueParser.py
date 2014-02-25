class sabQueueParser():

    def parse(self, response = {}):
        state = {"status":response["queue"]["status"],
                 "speed":response["queue"]["speed"],
                 "size_left":response["queue"]["sizeleft"],
                 "time_left":response["queue"]["timeleft"],
                 "mb":response["queue"]["mb"],
                 "mb":response["queue"]["mbleft"],
                 "downloaded": (float(response["queue"]['mb']) - float(response["queue"]['mbleft']) ) / 1024,
                 "total_queue": float(response["queue"]['mb']) / 1024,
                 "progress_pct": 100*( float(response["queue"]['mb']) - float(response["queue"]['mbleft'])) / (float(response["queue"]['mb'])+0.01),
                 "uptime": response["queue"]['uptime']
        }

        slots = []
        if response["queue"]['slots'] != None:
            try:
                response["queue"]['slots']['slot'].keys()
                slots = [ response["queue"]['slots']['slot'] ]
            except AttributeError:
                slots = response["queue"]['slots']['slot']

        queue = []
        for slot in slots:
            timeleft = slot['timeleft']
            if len(slot['timeleft']) == 7:
                timeleft = "0" + timeleft

            item = {"filename":slot["filename"],
                        "index":slot["index"],
                        "avg_age":slot["avg_age"],
                        "priority":slot["priority"],
                        "unpackopts":slot["unpackopts"],
                        "status":slot["status"],
                        "mb":slot["mb"],
                        "mb_left":slot["mbleft"],
                        "percentage":slot["percentage"],
                        "timeleft":timeleft
                        }

            queue.append(item)

        state["queue"] = queue
        return state