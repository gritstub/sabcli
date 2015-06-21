from mock import Mock
import nose
import BaseTestCase
from sabAPI import sabWarningsParser


class sabWarningsParser_Test(BaseTestCase.BaseTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()

        self.test_parser = sabWarningsParser.sabWarningsParser()

    def test_should_instantiate(self):
        assert (isinstance(self.test_parser, sabWarningsParser.sabWarningsParser))

    def test_parse_should_call_parseWarnings_to_extract_warning_details(self):
        self.test_parser.parseWarnings = Mock(return_value="warnings")
        response = {"warnings": []}

        result = self.test_parser.parse(response)

        self.test_parser.parseWarnings.assert_called_with(response["warnings"])

    def test_parseWarnings_should_extract_warning_details(self):
        warnings = ["12:00\nERROR\nmy warning"]

        result = self.test_parser.parseWarnings(warnings)

        assert (result == [{"timestamp": "12:00", "type": "ERROR", "message": "my warning"}])

    def test_parseWarnings_should_clean_warning_message(self):
        warnings = ["12:00\nERROR\nWARNING: filename=my.nzb warning, type=None"]

        result = self.test_parser.parseWarnings(warnings)

        assert (result == [{"timestamp": "12:00", "type": "ERROR", "message": "my.nzb warning"}])

if __name__ == '__main__':
    nose.runmodule()