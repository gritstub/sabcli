import sys

class sabEncoder( object ):
    def __init__(self):
        self.settings = sys.modules["__main__"].settings
        self.fetchpath = "/api?apikey=" + self.settings.apikey + "&mode="
        self.servername = self.settings.host + ":" + self.settings.port

    def encode(self, command, args = None,):
        ''' http://sabnzbdplus.wiki.sourceforge.net/Automation+Support '''
	
        url_fragment = command

        if args == None:
            if command in ('version', 'shutdown', 'restart'):
                url_fragment += ''
            elif command == 'queue':
                url_fragment += '&start=START&limit=LIMIT&output=xml'
            elif command == 'history':
                url_fragment += '&start=START&limit=LIMIT&output=xml'
            elif command == 'warnings':
                url_fragment += '&output=xml'
            elif command == 'pause':
                url_fragment = 'pause'
            elif command == 'resume':
                url_fragment = 'resume'
            else:
                self.stdscr.addstr('unhandled command: ' + command)
                usage(self, 2)

        url = 'http://' + self.servername + self.fetchpath + url_fragment
        return url

'''        elif len(args) == 1:
            if command in ('addlocalfile', 'addurl', 'addid'):
                url_fragment += '&name=' + args[0] + '&pp=' + self.job_option
            elif command == 'newapikey':
                if args[0] == 'confirm':
                    url_fragment = 'config&name=set_apikey'
                else:
                    url_fragment = ''
            elif command == 'queuecompleted':
                url_fragment = 'queue&name=change_complete_action&value=' + args[0]
            elif command == 'pathget':
                url_fragment = 'addlocalfile&name=' + args[0]
            elif command == 'delete':
                url_fragment = 'queue&name=delete&value=' + args[0]
            elif command == 'details':
                url_fragment = 'get_files&output=xml&value=' + args[0]
            elif command == 'speedlimit':
                url_fragment = 'config&name=speedlimit&value=' + args[0]
            elif command == 'autoshutdown':
                if args not in ('0', '1'):
                    return False
                else:
                    url_fragment += '&name=' + args[0]
            elif command == 'pause':
                url_fragment = 'queue&name=pause&value=' + args[0]
            elif command == 'temppause':
                url_fragment = 'config&name=set_pause&value=' + args[0]
            elif command == 'resume':
                url_fragment = 'queue&name=resume&value=' + args[0]
            elif command == 'history':
                if args[0] == 'clear':
                    url_fragment += '&name=delete&value=all'
                elif args[0].find('SABnzbd_nzo_') != -1:
                    url_fragment += '&name=delete&value=' + args[0]
                else:
                    usage(self, 2)
                    else:
                        self.stdscr.addstr('unhandled command: ' + command)
                        usage(self, 2)

                elif len(args) == 2:
                if command == 'rename':
                        url_fragment = 'queue&name=rename&value=' + str(args[0]) + '&value2=' + str(args[1])
                    elif command == 'priority':
                        url_fragment = 'queue&name=priority&value=' + str(args[0]) + '&value2=' + str(args[1])
                    elif command == 'postprocessing':
                        url_fragment = 'change_opts&value=' + str(args[0]) + '&value2=' + str(args[1])
                    elif command == 'move':
                        url_fragment = 'switch&value=' + str(args[0]) + '&value2=' + str(args[1])
                    else:
                        self.stdscr.addstr('unhandled command: ' + command)
                        usage(self, 2)
        else:
            self.stdscr.addstr('unhandled command: ' + command)
            usage(self, 2)

            self.url = 'http://' + self.servername + self.fetchpath + url_fragment

        data = self.__send_request(command, str(self.fetchpath + url_fragment).replace(' ', '%20'))

        if data == False and self.debug:
            self.stdscr.addstr(self.command_status)
            self.stdscr.refresh()
            time.sleep(5)

            return self.__parse_status(command, data)'''