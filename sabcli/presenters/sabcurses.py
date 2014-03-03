#!/usr/bin/env python
''' Command Line Interface for sabnzbd+

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    COPYING: http://www.gnu.org/licenses/gpl.txt

    Copyright 2010 Tobias Ussing

    Acknowledgements:
    Meethune Bhowmick - For the original code for the 0.4 api
    Henrik Mosgaard Jensen - For testing, critique layout and usability.
'''

# export TERM=linux; sabcurses.py

import os, sys, time, curses, traceback, signal
import getopt, ConfigParser
import curses.textpad

VERSION="0.7-1"
APIVERSION="0.7.11"

# TextColour
class tc:
    black = '\x1B[30;49m'
    red = "\x1B[31;49m"
    green = '\x1B[32;49m'
    yellow = '\x1B[33;49m'
    blue = '\x1B[34;49m'
    magenta = '\x1B[35;49m'
    cyan = '\x1B[36;49m'
    white = '\x1B[37;49m'
    bold = '\x1B[1;49m'
    end = '\x1B[m'

class SABnzbdCore( object ):
    ''' Sabnzbd Automation Class '''
    def __init__(self, config = None):
	self.config = config
        if not self.config:
            self.config = { 'host' : 'localhost', 'port' : '8080', 
                       'username' : None, 'password;' : None,
                       'apikey' : None }, 

        self.stdscr = curses.initscr()

        curses.start_color()
	curses.use_default_colors()
        curses.noecho()   
        curses.cbreak()   
        self.stdscr.keypad(1)
        curses.curs_set(0)

	#curses.color_pair(7)
	curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        curses.init_pair(4, curses.COLOR_YELLOW, -1)
        curses.init_pair(5, curses.COLOR_BLUE, -1)
        curses.init_pair(6, curses.COLOR_MAGENTA, -1)
        curses.init_pair(7, curses.COLOR_CYAN, -1)
        curses.init_pair(8, curses.COLOR_WHITE, -1)

        # Public Variables
        self.size = os.popen('stty size', 'r').read().split()
	self.win = curses.newwin(int(self.size[0]), int(self.size[1]), 0, 0)
	self.pad = curses.newpad(10000, int(self.size[1])-2)
        self.fetchpath = ''
        self.servername = ''
        self.header = {}
        self.postdata = None
        self.command_status = 'ok'
        self.return_data = {}
	self.last_fetch = {'fetch': '', 'refresh': 10, 'time': time.mktime(time.localtime())}
	self.retval = ''
	self.index = [-1, -1, -1, -1, -1, -1]
	self.indexCount = [-1, -1, -1, 5, -1, 2]
	self.historyID = []
	self.scroll = { 'firstline': 0, 'totallines': 0, 'item': [], 'lastitem': -1}
	self.details = {'move': None, 'nzo_id': [], 'filename': [], 'unpackopts': [], 'priority': [], 'newname': None}
	self.speedlimit = 0
        self.url = 'http://' + self.servername + '/sabnzbd/'
	self.job_option = '3'
	self.debug = None
	self.action = 0
	self.quit = 0
	self.view = 0
	self.selection = -1
	self.statusLine = ''
	self.disk = ''
	self.speed = ''
	self.newapikey = None
	signal.signal(signal.SIGWINCH, self.sigwinch_handler)

    # Private Methods        
    def sigwinch_handler(self, n, frame):
	self.last_fetch['fetch'] = ''
        self.size = os.popen('stty size', 'r').read().split()

    def xml_to_dict(self, el):
	d={}

    	if el.text:
	    d[el.tag] = el.text
    	else:
    	    d[el.tag] = None

    	for child in el:
	    if len(child):
            	if len(child) == 1 or child[0].tag != child[1].tag:
		    d[child.tag] = self.xml_to_dict(child)
		else:
		    temp = []
                    for subitem in child:
			if subitem.text != None:
	    		    temp.append(subitem.text)
			else:
			    temp2 = self.xml_to_dict(subitem)
			    temp.append(temp2)
			d[child.tag] = { subitem.tag : temp }
	    else:
		d[child.tag] = child.text

    	return d




def usage(sabnzbd, exitval):
    ''' Usage '''
    msg = sys.argv[0].split('/').pop()
    msg += " " + tc.cyan + "<command> <args>" + tc.end + "\n\n"
    msg += "Compatible with SABnzbd+: " + APIVERSION + "\n\n"
    msg += "Commands:\n\tpause " + tc.cyan + "[id]" + tc.end + "\n\tresume " + tc.cyan + "[id]" + tc.end + "\n\tshutdown\n\trestart\n\tversion\n\tqueue\t\t\t\t(watchable)\n\twarnings\t\t\t(watchable)\n\tdetails " + tc.cyan + "<id>" + tc.end + "\t\t\t(watchable)\n\tmove " + tc.cyan + "<id> <new position>" + tc.end + " \n"
    msg += "\thistory " + tc.cyan + "[clear]" + tc.end + "\t\t\t(watchable)\n\tnewapikey " + tc.cyan + "<confirm>" + tc.end + "\n\tspeedlimit " + tc.cyan + "<value>" + tc.end + "\n\tnewzbin " + tc.cyan + "<id>" + tc.end + "\n\taddurl " + tc.cyan + "<nzb url>" + tc.end + "\n\tpathget " + tc.cyan + "<nzb path>" + tc.end + "\n\ttemppause " + tc.cyan + "<minutes>" + tc.end + "\n"
    msg += "\trename " + tc.cyan + "<id> <newname>" + tc.end + "\n\tdelete " + tc.cyan + "<id>" + tc.end + "\t\t\t| all = clear queue. Multiple id's can be given\n\tpriority " + tc.cyan + "<id> <value>" + tc.end + "\t\t| -1 = Low, 0 = Normal, 1 = High, 2 = Force\n"
    msg += "\tpostprocessing " + tc.cyan + "<id> <value>" + tc.end + "\t| 0 = Skip, 1 = Repair, 2 = Unpack, 3 = Delete\n"
    msg += "\tqueuecompleted " + tc.cyan + "<path to script>" + tc.end + "\t| implemented, not confirmed\n";
    msg += "\nArguments:\n\t-h [--help]\t\t\tHelp screen\n\t-j [--job-option=3]\t\tSet job-option\n\t-H [--hostname=localhost]\tHostname\n\t-P [--port=8080]\t\tPort\n"
    msg += "\t-u [--username=user]\t\tUsername\n\t-p [--password=pass]\t\tPassword\n\t-a [--apikey=15433acd...]\tApikey\n\t-w [--watch=X]\t\t\tRerun command every X seconds\n\t\t\t\t\tStandard action is 'queue'\n\t\t\t\t\tCan watch all commands marked (watchable)\n"
    msg += "\nEnvironment variables:\n\tSABCLICFG=~/.nzbrc (default)\n\tDEBUG=1\t\t\t\t| Enable debug\n"

    sabnzbd.stdscr.addstr(msg + '\n')
    sys.exit(exitval)

def parse_options(sabnzbd, options):
    ''' Parse Cli options '''
    default_opts = ("hj:H:P:u:p:a:w:" , ["help" , "job-option=", "hostname=", "port=", "username=", "password=", "apikey=", "watch="])
    command = None
    command_args = None

    try:
        opt , args = getopt.getopt(options, default_opts[0], default_opts[1])
    except getopt.GetoptError:
        usage(self, OB2)
    for option , arguement in opt:
        if option in ("-h", "--help"):
            usage(self, 2)
        elif option in ("-j", "--job-option"):
            self.job_option = str(arguement)
        elif option in ("-H", "--hostname"):
            sabnzbd.config['host'] = str(arguement)
        elif option in ("-P", "--port"):
            sabnzbd.config['port'] = str(arguement)
        elif option in ("-u", "--username"):
            sabnzbd.config['password'] = str(arguement)
        elif option in ("-p", "--password"):
            sabnzbd.config['password'] = str(arguement)
        elif option in ("-a", "--apikey"):
            sabnzbd.config['apikey'] = str(arguement)

def parse_config(config):
    ''' Parse config file for server info '''
    parser = ConfigParser.ConfigParser()
    config_dict = {}
    try:
        config_file = open(config)
        parser.readfp(config_file)
        config_file.close()
    except IOError:
	usage(self, 1)
        sys.stderr.write('Unable to open ' + config + '\n')


    try:
        for each in ('host', 'port', 'username', 'password', 'apikey'):
            config_dict[each] = parser._get('server', each)
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        sys.stderr.write('Unable to parse ' + config + '\n')
        sys.stderr.write('Format should be:\n')
        sys.stderr.write('[server]\n')
        sys.stderr.write('host = <sabnzbd server>\n')
        sys.stderr.write('port = <sabnzbd port>\n')
        sys.stderr.write('username = <sabnzbd name> | None\n')
        sys.stderr.write('password = <sabnzbd password> | None\n') 
        sys.stderr.write('apikey = <sabnzbd apikey> | None\n') 
        usage(self, 1)

    return config_dict

def editfield(editwin):
    curses.curs_set(1)
    newname = curses.textpad.Textbox(editwin, insert_mode = True).edit().strip()
    curses.curs_set(0)

    return newname

def restorescreen(sabnzbd):
    # Cleanup of exit for FreeBSD.
    #sabnzbd.stdscr.addstr(int(sabnzbd.size[0])-1, 0, " " * (int(sabnzbd.size[1])-1) )                                                                    
    #sabnzbd.stdscr.refresh()
    curses.curs_set(1)
    curses.nocbreak();
    sabnzbd.stdscr.keypad(0);
    curses.echo()
    curses.endwin()
    sys.stderr.write(sabnzbd.size[0] + " - " + sabnzbd.size[1] + "\n")

def mainloop(sabnzbd):
        sabnzbd.printMenu()
        command = 0
        sabnzbd.action = 0
	help = -1
        while sabnzbd.quit == 0:
            sabnzbd.display()
	    delay = int((sabnzbd.last_fetch['refresh'] - ( time.mktime(time.localtime()) - sabnzbd.last_fetch['time'] )) * 1000 + 100)
	    if delay > 10100:
		delay = 10100
	    if sabnzbd.quit:
		delay = 100;
	    sabnzbd.stdscr.timeout(delay)
            c = sabnzbd.stdscr.getch()
	    sabnzbd.action = 0
            if help != -1:
                sabnzbd.view = help
                help = -2
            if c == ord('Q'): sabnzbd.quit = 1 # quit
            elif c == ord('1'): sabnzbd.view = 0 # queue
            elif c == ord('2'): sabnzbd.view = 1 # history
            elif c == ord('3'): sabnzbd.view = 2 # warnings
            elif c == ord('4'): sabnzbd.view = 3 # more
            elif c == ord('5'): sabnzbd.view = 4 # help
	    elif c == ord('?'):
		if help == -1: help = sabnzbd.view; sabnzbd.view = 4; # help
            elif c == ord('p'): sabnzbd.action = 4 # pause
            elif c == ord('r'): sabnzbd.action = 5 # resume
            elif c in ( 330, 263, 127): sabnzbd.action = 6 # delete #263 (backspace linux) #127 (backspace freebsd) 330 (delete freebsd/linux)
            elif c == ord('S'): sabnzbd.action = 7 # shutdown
            elif c == ord('R'): sabnzbd.action = 8 # restart
	    elif c == ord('m'): sabnzbd.action = 9 # move
            elif c == ord('h') and sabnzbd.view == 0:
                sabnzbd.view = 5
                sabnzbd.action = 11
                sabnzbd.details['priority'][sabnzbd.index[sabnzbd.view]] = -1 # priority
            elif c == ord('j') and sabnzbd.view == 0:
                sabnzbd.view = 5
                sabnzbd.action = 11
                sabnzbd.details['priority'][sabnzbd.index[sabnzbd.view]] = 0 # priority
            elif c == ord('k') and sabnzbd.view == 0:
                sabnzbd.view = 5
                sabnzbd.action = 11
                sabnzbd.details['priority'][sabnzbd.index[sabnzbd.view]] = 1 # priority
            elif c == ord('l') and sabnzbd.view == 0 and sabnzbd.index[sabnzbd.view] != -1:
                sabnzbd.view = 5
                sabnzbd.action = 11
                sabnzbd.details['priority'][sabnzbd.index[sabnzbd.view]] = 2 # priority
            elif c == ord('H') and sabnzbd.view == 0 and sabnzbd.index[sabnzbd.view] != -1:
                sabnzbd.view = 5
                sabnzbd.action = 12
                sabnzbd.details['unpackopts'][sabnzbd.index[sabnzbd.view]] = 0 # postprocessing
            elif c == ord('J') and sabnzbd.view == 0 and sabnzbd.index[sabnzbd.view] != -1:
                sabnzbd.view = 5
                sabnzbd.action = 12
                sabnzbd.details['unpackopts'][sabnzbd.index[sabnzbd.view]] = 1 # postprocessing
            elif c == ord('K') and sabnzbd.view == 0 and sabnzbd.index[sabnzbd.view] != -1:
                sabnzbd.view = 5
                sabnzbd.action = 12
                sabnzbd.details['unpackopts'][sabnzbd.index[sabnzbd.view]] = 2 # postprocessing
            elif c == ord('L') and sabnzbd.view == 0 and sabnzbd.index[sabnzbd.view] != -1:
                sabnzbd.view = 5
                sabnzbd.action = 12
                sabnzbd.details['unpackopts'][sabnzbd.index[sabnzbd.view]] = 3 # postprocessing
	    elif c == ord('d'):
                if sabnzbd.view == 0 and sabnzbd.index[sabnzbd.view] > -1:
                    sabnzbd.view = 5
                    sabnzbd.index[sabnzbd.view] = -1
		elif sabnzbd.view == 5:
		    sabnzbd.view = 0
	# Curser up
            elif c == 259: 
		if sabnzbd.view in ( 0, 1, 2, 3, 4, 5 ) and sabnzbd.selection == -1:
                    if sabnzbd.index[sabnzbd.view] > -1:
                        sabnzbd.index[sabnzbd.view] = sabnzbd.index[sabnzbd.view] - 1
                    else:
                        sabnzbd.index[sabnzbd.view] = sabnzbd.indexCount[sabnzbd.view] 
		if sabnzbd.view == 0 and sabnzbd.selection == 1 and sabnzbd.details['priority'][sabnzbd.index[0]] < 2:
			sabnzbd.details['priority'][sabnzbd.index[0]] += 1
			sabnzbd.action = 11
                if sabnzbd.view == 0 and sabnzbd.selection == 2 and sabnzbd.details['unpackopts'][sabnzbd.index[0]] > 0:
                        sabnzbd.details['unpackopts'][sabnzbd.index[0]] -= 1
                        sabnzbd.action = 12
	# Curser down
            elif c == 258: 
            	if sabnzbd.view in ( 0, 1, 2, 3, 4, 5 ) and sabnzbd.selection == -1:
                    if sabnzbd.index[sabnzbd.view] < sabnzbd.indexCount[sabnzbd.view]:
                        sabnzbd.index[sabnzbd.view] = sabnzbd.index[sabnzbd.view] + 1
                    else:
                        sabnzbd.index[sabnzbd.view] = -1
		if sabnzbd.view == 0 and sabnzbd.selection == 1 and sabnzbd.details['priority'][sabnzbd.index[0]] > -1:
			sabnzbd.details['priority'][sabnzbd.index[0]] -= 1
			sabnzbd.action = 11
                if sabnzbd.view == 0 and sabnzbd.selection == 2 and sabnzbd.details['unpackopts'][sabnzbd.index[0]] < 3:
                        sabnzbd.details['unpackopts'][sabnzbd.index[0]] += 1
                        sabnzbd.action = 12
	# Curser left
            elif c == 260: 
            	if ( sabnzbd.view == 0 and sabnzbd.index[sabnzbd.view] > -1 ) or ( sabnzbd.view == 5 and sabnzbd.index[sabnzbd.view] == -1 ):
                    sabnzbd.action = 0
                    sabnzbd.view = 0
		    if sabnzbd.selection > -1:
			sabnzbd.selection -= 1
		    if sabnzbd.selection == -1:
			sabnzbd.selection = -2
            	if sabnzbd.view == 5 and sabnzbd.index[sabnzbd.view] == 0:
		    if sabnzbd.details['priority'][sabnzbd.index[0]] > -1:
			sabnzbd.details['priority'][sabnzbd.index[0]] -= 1
                if sabnzbd.view == 5 and sabnzbd.index[sabnzbd.view] == 1: 
		    if sabnzbd.details['unpackopts'][sabnzbd.index[0]] > 0:
			sabnzbd.details['unpackopts'][sabnzbd.index[0]] -= 1
	# Curser right
            elif c == 261: 
            	if sabnzbd.view == 0 and sabnzbd.index[sabnzbd.view] > -1:
		    if sabnzbd.selection < 2:
			sabnzbd.selection += 1
                if sabnzbd.view == 5 and sabnzbd.index[sabnzbd.view] == 0: 
                    if sabnzbd.details['priority'][sabnzbd.index[0]] < 2:
                        sabnzbd.details['priority'][sabnzbd.index[0]] += 1
                if sabnzbd.view == 5 and sabnzbd.index[sabnzbd.view] == 1:
                    if sabnzbd.details['unpackopts'][sabnzbd.index[0]] < 3:
                        sabnzbd.details['unpackopts'][sabnzbd.index[0]] += 1
	# Page up
            elif c == 339: 
            	if sabnzbd.index[sabnzbd.view] -5 > -1:
                    sabnzbd.index[sabnzbd.view] = sabnzbd.index[sabnzbd.view] - 5
                else:
                    sabnzbd.index[sabnzbd.view] = -1
	# Page down
            elif c == 338: 
            	if sabnzbd.index[sabnzbd.view] == -1:
		    if sabnzbd.indexCount[sabnzbd.view] >= 5:
			sabnzbd.index[sabnzbd.view] = 5
		    else:
			sabnzbd.index[sabnzbd.view] = sabnzbd.indexCount[sabnzbd.view]
            	elif sabnzbd.index[sabnzbd.view] +5 <= sabnzbd.indexCount[sabnzbd.view]:
                    sabnzbd.index[sabnzbd.view] = sabnzbd.index[sabnzbd.view] + 5
            	else:
                    sabnzbd.index[sabnzbd.view] = sabnzbd.indexCount[sabnzbd.view] 

        # Home
            elif c == 262:
		sabnzbd.index[sabnzbd.view] = -1
        # Home   
            elif c in ( 360, 385 ):
                sabnzbd.index[sabnzbd.view] = sabnzbd.indexCount[sabnzbd.view]

	# Space
	    elif c == 32:
                if sabnzbd.view == 0:
                    if sabnzbd.selection == -1:
                        sabnzbd.action = 9
	# Enter
            elif c == 10:
		if sabnzbd.view == 0:
		    if sabnzbd.selection == 0:
			line = 4 + sabnzbd.scroll['item'][sabnzbd.index[sabnzbd.view]][0]
			editwin = sabnzbd.win.subwin(1, int(sabnzbd.size[1])-33, line, 7)
			editwin.addstr(0, 0, ' ' * ( int(sabnzbd.size[1]) - 34 ) )
                        editwin.addstr(0, 0, sabnzbd.details['filename'][sabnzbd.index[0]][:( int(sabnzbd.size[1]) - 34 )])
			newname = editfield(editwin)
			if newname != '':
			    sabnzbd.details['newname'] = newname
			    sabnzbd.action = 10

                if sabnzbd.view == 5 and sabnzbd.index[sabnzbd.view] == 0:
                    sabnzbd.action = 11

                if sabnzbd.view == 5 and sabnzbd.index[sabnzbd.view] == 1:
                    sabnzbd.action = 12

            	if sabnzbd.view == 5 and sabnzbd.index[sabnzbd.view] == 2:	
		    editwin = sabnzbd.win.subwin(1, int(sabnzbd.size[1])-33, 4, 33)
		    editwin.addstr(0, 0, ' ' * ( int(sabnzbd.size[1]) - 34 ) )
		    editwin.addstr(0, 0, sabnzbd.details['filename'][sabnzbd.index[0]])

		    newname = editfield(editwin)

		    if newname != '':
			sabnzbd.details['newname'] = newname
			sabnzbd.action = 10

		# More view
		if sabnzbd.view == 3:
		    posy = 0
		    posx = 0
		    width = int(sabnzbd.size[1])-40
		    if sabnzbd.index[sabnzbd.view] == 0:
			posy = 5
			posx = 22
		    elif sabnzbd.index[sabnzbd.view] == 1:
			posy = 8
			posx = 21
                    elif sabnzbd.index[sabnzbd.view] == 2:
                        posy = 11
                        posx = 20
			width = 7
                    elif sabnzbd.index[sabnzbd.view] == 3:
                        posy = 14
                        posx = 19
			width = 5
                    elif sabnzbd.index[sabnzbd.view] == 4:
                        posy = 17
                        posx = 15
                    elif sabnzbd.index[sabnzbd.view] == 5:
                        posy = 20
                        posx = 24
			width = 4
			
		    editwin = sabnzbd.win.subwin(1, width, posy , posx)
		    editwin.addstr(0, 0, ' ' * ( width - 1 ) )
		    editwin.addstr(0, 0, '')
		    data = editfield(editwin)
		    sabnzbd.action = 0

		    if sabnzbd.index[sabnzbd.view] == 0:
			# Add file or link
			if data.find('http') > -1:
			    sabnzbd.run_commands('addurl', [data])
			else:
			    sabnzbd.run_commands('addlocalfile', [data])

		    elif sabnzbd.index[sabnzbd.view] == 1:
			# add newzbin
			sabnzbd.run_commands('addid', [data])

		    elif sabnzbd.index[sabnzbd.view] == 2:
			# set speed limit
			try:
			    if data == '':
				data = '0'
			    if data == '0':
				sabnzbd.speedlimit = None
			    else:
				sabnzbd.speedlimit = int(data)
			    sabnzbd.run_commands('speedlimit', [data])
			except ValueError:
			    sabnzbd.speedlimit = None

		    elif sabnzbd.index[sabnzbd.view] == 3:
			# set temporary pause
			sabnzbd.run_commands('temppause', [data])

		    elif sabnzbd.index[sabnzbd.view] == 4:
			# queue complete script
                        sabnzbd.run_commands('queuecompleted', [data])

		    elif sabnzbd.index[sabnzbd.view] == 5:
			if data == 'yes':
			    sabnzbd.run_commands('newapikey', ['confirm'])
			    sabnzbd.quit = 1 # quit

            elif c != -1:
		if sabnzbd.debug:
		    sabnzbd.stdscr.addstr(1, 0, 'Captured key: ' + str(c))
		    sabnzbd.stdscr.refresh()
		    time.sleep(2)

	    if help == -2:
		help = -1

def main():
    ''' Command line front end to sabnzbd+ '''
    configFile = os.environ._get("SABCLICFG");
    if configFile == None:
        configFile = os.environ['HOME'] + "/.nzbrc"
    commands = None
            
    if not os.path.exists(configFile):
        sys.stderr.write('\nUnable to open ' + configFile + '\n\n')
    else:   
        config_dict = parse_config(configFile)
        sabnzbd = SABnzbdCore(config_dict)
        sabnzbd.debug = os.environ._get("DEBUG");
	parse_options(sabnzbd, sys.argv[1:])
        sabnzbd.setConnectionVariables()

	try:
	    mainloop(sabnzbd)
	    restorescreen(sabnzbd)
	except:
	    restorescreen(sabnzbd)
	    traceback.print_exc()

	if sabnzbd.newapikey != None:
	    print 'New API key: ' + str(sabnzbd.newapikey)

if __name__ == '__main__':
    main()
#    cProfile.run('main()')
    sys.exit(0)
