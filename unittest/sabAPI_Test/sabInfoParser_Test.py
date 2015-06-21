import nose
import BaseTestCase
from sabAPI import sabInfoParser


class sabInfoParser_Test(BaseTestCase.BaseTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()

        self.test_parser = sabInfoParser.sabInfoParser()

    def test_should_instantiate(self):
        assert (isinstance(self.test_parser, sabInfoParser.sabInfoParser))

    def test_parse_should_return_canned_response(self):
        result = self.test_parser.parse({})

        assert (result == {"version": '1.0', "speedlimit": "None"})

if __name__ == '__main__':
    nose.runmodule()