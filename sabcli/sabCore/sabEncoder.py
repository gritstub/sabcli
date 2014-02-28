import sys

class sabEncoder( object ):
    def __init__(self):
        self.settings = sys.modules["__main__"].settings
        self.fetchpath = "/api?apikey=" + self.settings.apikey + "&mode="
        self.servername = self.settings.host + ":" + self.settings.port
        self.output = "&output=json"

    def encodeQuery(self, command):
        ''' http://sabnzbdplus.wiki.sourceforge.net/Automation+Support '''
        url_fragment = command

        if command in ('version', 'shutdown', 'restart', 'warnings'):
            url_fragment += ''
        elif command == 'queue':
            url_fragment += '&start=START&limit=LIMIT'
        elif command == 'history':
            url_fragment += '&start=START&limit=LIMIT'
        elif command == 'pause':
            url_fragment = 'pause'
        elif command == 'resume':
            url_fragment = 'resume'
        else:
            self.stdscr.addstr('unhandled command: ' + command)

        url = 'http://' + self.servername + self.fetchpath + url_fragment + self.output
        return url

    def encodeQueueAction(self, command, args):
        url_fragment = command
        if len(args) == 1:
            if command == 'queuecompleted':
                url_fragment = 'queue&name=change_complete_action&value=' + args[0]
            elif command == 'delete':
                url_fragment = 'queue&name=delete&value=' + args[0]
            elif command == 'details':
                url_fragment = 'get_files&output=xml&value=' + args[0]
            elif command == 'pause':
                url_fragment = 'queue&name=pause&value=' + args[0]
            elif command == 'resume':
                url_fragment = 'queue&name=resume&value=' + args[0]

        if len(args) == 2:
            if command == 'rename':
                url_fragment = 'queue&name=rename&value=' + str(args[0]) + '&value2=' + str(args[1])
            elif command == 'priority':
                url_fragment = 'queue&name=priority&value=' + str(args[0]) + '&value2=' + str(args[1])
            elif command == 'postprocessing':
                url_fragment = 'change_opts&value=' + str(args[0]) + '&value2=' + str(args[1])
            elif command == 'move':
                url_fragment = 'switch&value=' + str(args[0]) + '&value2=' + str(args[1])

        url = 'http://' + self.servername + self.fetchpath + url_fragment
        return url

    def encodeHistoryAction(self, command, args):
        url_fragment = command

        if command == 'history':
            if args[0] == 'clear':
                url_fragment += '&name=delete&value=all'
            elif args[0].find('SABnzbd_nzo_') != -1:
                url_fragment += '&name=delete&value=' + args[0]

        url = 'http://' + self.servername + self.fetchpath + url_fragment
        return url

    def encodeMiscAction(self, command, args):
        url_fragment = command

        if command in ('addlocalfile', 'addurl', 'addid'):
            url_fragment += '&name=' + args[0]
        elif command == 'newapikey':
            if args[0] == 'confirm':
                url_fragment = 'config&name=set_apikey'
            else:
                url_fragment = ''

        elif command == 'temppause':
            url_fragment = 'config&name=set_pause&value=' + args[0]

        elif command == 'pathget':
            url_fragment = 'addlocalfile&name=' + args[0]

        elif command == 'speedlimit':
            url_fragment = 'config&name=speedlimit&value=' + args[0]

        elif command == 'autoshutdown':
            if args not in ('0', '1'):
                return False
            else:
                url_fragment += '&name=' + args[0]

        url = 'http://' + self.servername + self.fetchpath + url_fragment
        return url