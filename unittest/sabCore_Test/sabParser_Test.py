import nose
from mock import patch
import BaseTestCase
from sabCore import sabParser


class sabParser_Test(BaseTestCase.BaseTestCase):

    def setUp(self):
        self.test_parser = sabParser.sabParser()

    def test_should_instantiate(self):
        assert(isinstance(self.test_parser, sabParser.sabParser))

    @patch('sabCore.sabParser.json.loads')
    def test_should_parse_using_json(self, mock_loads):
        self.test_parser.parse("string")

        mock_loads.assert_called_once_with("string")


    @patch('sabCore.sabParser.json.loads')
    def test_should_not_do_any_postprocessing(self, mock_loads):
        mock_loads.return_value = {"string"}

        value = self.test_parser.parse("string")

        assert (value == {"string"})

if __name__ == '__main__':
    nose.runmodule()