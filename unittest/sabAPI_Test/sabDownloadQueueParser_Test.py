import json
import nose
import BaseTestCase
from sabAPI.sabDownloadQueueParser import sabDownloadQueueParser


class sabDownloadQueueParser_Test(BaseTestCase.BaseTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()

        self.test_parser = sabDownloadQueueParser()

    def test_should_instantiate(self):
        assert (isinstance(self.test_parser, sabDownloadQueueParser))

    def test_parse_should_extract_general_queue_state(self):
        with open('data/queue.json') as f:
            response = json.load(f)

        result = self.test_parser.parse(response)

        assert (result["status"] == "Downloading")
        assert (result["speed"] == "1296.02 kb/s")
        assert (result["size_left"] == "1.2 GB")
        assert (result["time_left"] == "0:16:44")
        assert (result["mb"] == "1277.65")
        assert (result["mbleft"] == "1271.58")
        assert (result["diskspace2"] == "161.16")
        assert (result["diskspacetotal2"] == "465.21")
        assert (result["downloaded"] == 0.00592773437500016)
        assert (result["total_queue"] == 1.247705078125)
        assert (result["progress_pct"] == 0.47508726891349523)

    def test_parseQueue_should_extract_queue_details(self):
        with open('data/queue.json') as f:
            response = json.load(f)

        result = self.test_parser.parse(response)

        assert (result["queue"][0]["filename"] == "TV.Show.S04E11.720p.HDTV.x264")
        assert (result["queue"][0]["index"] == 0)
        assert (result["queue"][0]["avg_age"] == "2895d")
        assert (result["queue"][0]["priority"] == "Normal")
        assert (result["queue"][0]["unpackopts"] == 3)
        assert (result["queue"][0]["status"] == "Downloading")
        assert (result["queue"][0]["mb"] == "1277.65")
        assert (result["queue"][0]["id"] == "SABnzbd_nzo_p86tgx")
        assert (result["queue"][0]["mb_left"] == "1271.59")
        assert (result["queue"][0]["percentage"] == "0")
        assert (result["queue"][0]["timeleft"] == "00:16:44")
        assert (result["queue"][1]["filename"] == "TV.Show.S04E12.720p.HDTV.x264")
        assert (result["queue"][1]["index"] == 1)
        assert (result["queue"][1]["avg_age"] == "2895d")
        assert (result["queue"][1]["priority"] == "Normal")
        assert (result["queue"][1]["unpackopts"] == 3)
        assert (result["queue"][1]["status"] == "Paused")
        assert (result["queue"][1]["mb"] == "1277.76")
        assert (result["queue"][1]["id"] == "SABnzbd_nzo_ksfai6")
        assert (result["queue"][1]["mb_left"] == "1277.76")
        assert (result["queue"][1]["percentage"] == "0")
        assert (result["queue"][1]["timeleft"] == "00:00:00")

if __name__ == '__main__':
    nose.runmodule()