import json
import nose
import BaseTestCase
from sabAPI import sabWarningsParser


class sabWarningsParser_Test(BaseTestCase.BaseTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()

        self.test_parser = sabWarningsParser.sabWarningsParser()

    def test_should_instantiate(self):
        assert (isinstance(self.test_parser, sabWarningsParser.sabWarningsParser))

    def test_parseWarnings_should_extract_warning_details(self):
        with open('data/warnings.json') as f:
            response = json.load(f)

        result = self.test_parser.parse(response)

        assert (result["warnings"][0]["message"] == "API key missing, please enter the API key from Config->General into your 3rd party program")
        assert (result["warnings"][0]["timestamp"] == "2017-09-11 11:11:29")
        assert (result["warnings"][0]["type"] == "WARNING")

if __name__ == '__main__':
    nose.runmodule()