from cursesUI.cursesWindow import cursesWindow


class sabMiscPresenter():
    def __init__(self, window = None):
        if not window:
            window = cursesWindow()
        self.window = window

        self.screen = []
        self.pad = []

    def display(self, apiInfo = {}):
        self.screen = []
        self.pad = []

        self.displayGeneralInformation(apiInfo)
        self.displayMiscellaneousInformation(apiInfo)

        self.window.draw(self.screen)
        self.window.pad.draw(self.pad)

    def displayGeneralInformation(self, apiInfo):
        self.screen.append((3, 2, 'Option - Description\n', ''))
        version = 'SABCurses: ' + apiInfo['version']
        self.screen.append((int(self.window.size[1]) - len(version), 2, version, ''))
        self.screen.append((0, 3, '-' * int(self.window.size[1] + '\n'), ''))

    def displayMiscellaneousInformation(self, apiInfo):
        self.pad.append((3,  0, 'Add file or link', ''))
        self.pad.append((35, 0, '- Add a nzb file location or URL to sabnzbd+', ''))
        self.pad.append((8,  1, 'URL or file :', ''))

        self.pad.append((3,  3, 'Add newzbin', ''))
        self.pad.append((35, 3, '- Add a nzb from Newzbin.com to sabnzbd+ by entering a Newzbin Id', ''))
        self.pad.append((8,  4, 'Newzbin ID :', ''))

        self.pad.append((3,  6, 'Speed limit: ' + apiInfo["speedlimit"], ''))
        self.pad.append((35, 6, '- Limit the download speed of sabnzbd+ (Useful to avoid network congestion)', ''))
        self.pad.append((8,  7, 'New limit :', ''))

        self.pad.append((3,  9, 'Set temporary pause', ''))
        self.pad.append((35, 9, '- Pause queue for X minutes\n', ''))
        self.pad.append((8,  10, 'Duration :', ''))

        self.pad.append((3,  12, 'Set queue completed script', ''))
        self.pad.append((35, 12, '- Enter path to a local shell script that will be executed once sabnzbd+ finishes its queue\n\n', ''))
        self.pad.append((8,  13, 'Path :', ''))

        self.pad.append((3,  15, "Generate newapikey", ''))
        self.pad.append((35, 15, '- Change the current API Key of sabnzbd+ (WARNING this will disable use of SABCurses)\n', ''))
        self.pad.append((8,  16, 'Are you Sure? :', ''))
        self.pad.append((35, 16, "- Write 'yes' to confirm", ''))

'''
#        if APIVERSION != self.retval:
#            self.stdscr.addstr(1, 3, "WARNING:", curses.color_pair(2))
#            self.stdscr.addstr(" API version mismatch between SABCurses (%s) and daemon (%s)" % (APIVERSION, self.retval ) )

'''