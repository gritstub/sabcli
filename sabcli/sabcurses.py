#!/usr/bin/env python
import sys
import os
import traceback


def getConfigFileLocation():
    result = os.environ.get("SABCLICFG");

    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        result = sys.argv[1]

    if result is None:
        result = os.environ['HOME'] + "/.nzbrc"

    if not os.path.exists(result):
        sys.stderr.write('\nUnable to open ' + result + '\n\n')
        exit(0)
    return result


def tryToRecoverTerminal():
    try:
        from cursesUI.cursesWindow import cursesWindow
        tmp = cursesWindow()
        tmp.initialize()
        tmp.close()
    except:
        pass


if __name__ == '__main__':
    sys.modules["__main__"].configFile = getConfigFileLocation()
    from controllers.sabController import sabController
    controller = sabController()

    if len(sys.argv) > 2:
        controller.debug = True

    try:
        controller.run()
    except Exception as e:
        tryToRecoverTerminal()
        print repr(e)
        traceback.print_tb(sys.exc_info()[2])