import nose
import BaseTestCase
from sabAPI import sabInfoParser


class sabInfoParser_Test(BaseTestCase.BaseTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()

        self.test_parser = sabInfoParser.sabInfoParser()

    def test_should_instantiate(self):
        assert (isinstance(self.test_parser, sabInfoParser.sabInfoParser))

if __name__ == '__main__':
    nose.runmodule()