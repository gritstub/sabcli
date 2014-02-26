import  sys

class sabMiscPresenter():
    def __init__(self):
        self.window = sys.modules["__main__"].window

    def display(self, apiInfo = {}):
        self.window.addString(2, 3, 'Option - Description\n')
        version = 'SABCurses: ' + apiInfo['version']
        self.window.addString(2, int(self.window.size[1]) - len(version), version)
        self.window.addString(3, 0, '-' * int(self.window.size[1] + '\n'))
        self.window.addStr('\n')

        self.window.pad.addStr('   Add file or link')
        self.window.pad.addString(0, 35, '- Add a nzb file location or URL to sabnzbd+')
        self.window.pad.addString(1, 8, 'URL or file :\n\n')

        self.window.pad.addStr('   Add newzbin')
        self.window.pad.addString(3, 35, '- Add a nzb from Newzbin.com to sabnzbd+ by entering a Newzbin Id')
        self.window.pad.addString(4, 8, 'Newzbin ID :\n\n')

        self.window.pad.addStr('   Speed limit: ' + apiInfo["speedlimit"])
        self.window.pad.addString(6, 35, '- Limit the download speed of sabnzbd+ (Useful to avoid network congestion)')
        self.window.pad.addString(7, 8, 'New limit :\n\n')

        self.window.pad.addStr('   Set temporary pause')
        self.window.pad.addString(9, 35, '- Pause queue for X minutes\n')
        self.window.pad.addString(10, 8, 'Duration :\n\n')

        self.window.pad.addStr('   Set queue completed script')
        self.window.pad.addString(12, 35, '- Enter path to a local shell script that will be executed once sabnzbd+ finishes its queue\n\n')
        self.window.pad.addString(13, 8, 'Path :\n\n')

        self.window.pad.addStr("   Generate newapikey")
        self.window.pad.addString(15, 35, '- Change the current API Key of sabnzbd+ (WARNING this will disable use of SABCurses)\n')
        self.window.pad.addString(16, 8, 'Are you Sure? :\n')
        self.window.pad.addString(16, 35, "- Write 'yes' to confirm")

        return True

    '''
    #        self.run_commands('version',  None)

#        if APIVERSION != self.retval:
#            self.stdscr.addstr(1, 3, "WARNING:", curses.color_pair(2))
#            self.stdscr.addstr(" API version mismatch between SABCurses (%s) and daemon (%s)" % (APIVERSION, self.retval ) )

'''