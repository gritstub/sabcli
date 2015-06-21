import sys
import unittest
import io

sys.path.append('../sabcli/')
sys.path.append('../sab-mocks/')


class BaseTestCase(unittest.TestCase):#pragma: no cover

    def setUp(self):
        sys.modules["__main__"].configFile = "temp"

    def readTestInput(self, filename, should_eval = True):
        try:
            testinput = open("resources/" + filename)
            inputdata = testinput.read()
        except:
            testinput = io.open("resources/" + filename)
            inputdata = testinput.read()

        if should_eval:
            inputdata = eval(inputdata)
        return inputdata

    def raiseError(self, exception):
        raise exception