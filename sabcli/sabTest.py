#!/usr/bin/env python
import sys
import os
import traceback

configFile = ""

def buildDependencyGraph():
    from configuration import configuration
    sys.modules["__main__"].settings = configuration(configFile)

    loadCoreLayer()

    loadAPILayer()

    #loadPresentationLayer()

    #loadControlLayer()

def loadCoreLayer():
    from sabCore.sabChannel import sabChannel
    sys.modules["__main__"].channel = sabChannel()

    from sabCore.sabEncoder import sabEncoder
    sys.modules["__main__"].encoder = sabEncoder()

    from sabCore.sabParser import sabParser
    sys.modules["__main__"].parser = sabParser()

    from sabCore.sabCore import sabCore
    sys.modules["__main__"].core = sabCore()

def loadAPILayer():
    from sabAPI.sabInfoParser import sabInfoParser
    sys.modules["__main__"].infoParser = sabInfoParser()

    from sabAPI.sabQueueParser import sabQueueParser
    sys.modules["__main__"].queueParser = sabQueueParser()

    from sabAPI.sabHistoryParser import sabHistoryParser
    sys.modules["__main__"].historyParser = sabHistoryParser()

    from sabAPI.sabWarningsParser import sabWarningsParser
    sys.modules["__main__"].warningsParser = sabWarningsParser()

    from sabAPI.sabAPI import sabAPI
    api = sabAPI()
    sys.modules["__main__"].api = api


def loadPresentationLayer():
    sys.modules["__main__"].pad = ""

    from presenters.sabWindow import sabWindow
    window = sabWindow()
    sys.modules["__main__"].window = window

    from presenters.sabStatusPresenter import sabStatusPresenter
    sys.modules["__main__"].statusPresenter = sabStatusPresenter()

    from presenters.sabScrollPresenter import sabScrollPresenter
    sys.modules["__main__"].scroller = sabScrollPresenter()

    from presenters.sabNavigationControl import sabNavigationControl
    sys.modules["__main__"].navigation = sabNavigationControl()

    from presenters.sabQueuePresenter import sabQueuePresenter
    sys.modules["__main__"].queuePresenter = sabQueuePresenter()

    from presenters.sabHelpPresenter import sabHelpPresenter
    sys.modules["__main__"].helpPresenter = sabHelpPresenter()

    from presenters.sabMiscPresenter import sabMiscPresenter
    sys.modules["__main__"].miscPresenter = sabMiscPresenter()

def loadControlLayer():
    from controllers.sabStatusController import sabStatusController
    sys.modules["__main__"].statusController = sabStatusController()

    from controllers.sabHelpController import sabHelpController
    sys.modules["__main__"].helpController = sabHelpController()

    from controllers.sabQueueController import sabQueueController
    sys.modules["__main__"].queueController = sabQueueController()

    from controllers.sabMiscController import sabMiscController
    sys.modules["__main__"].miscController = sabMiscController()

    from controllers.sabController import sabController
    controller = sabController()

    sys.modules["__main__"].controller = controller


def getConfigFileLocation():
    result = os.environ.get("SABCLICFG");
    if sys.argv[1] and os.path.exists(sys.argv[1]):
        result = sys.argv[1]
    if result == None:
        result = os.environ['HOME'] + "/.nzbrc"
    if not os.path.exists(result):
        sys.stderr.write('\nUnable to open ' + result + '\n\n')
        exit(0)
    return result


if __name__ == '__main__':
    configFile = getConfigFileLocation()
    buildDependencyGraph()

    try:
        tmp = api.getApiInfo()
    except Exception as e:
        print repr(e)
        traceback.print_tb(sys.exc_info()[2])