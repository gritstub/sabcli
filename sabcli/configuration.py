import sys
import argparse
from ConfigParser import ConfigParser


class configuration():
    def __init__(self):
        self.extractServerConnectionDetailsFromConfiguration(sys.modules["__main__"].configFile)
        self.overrideServerConnectionDetailsFromCommandLine()

    def overrideServerConnectionDetailsFromCommandLine(self):
        parser = argparse.ArgumentParser(description='Curses client for SABnzbd+')
        parser.add_argument('-H', '--hostname')
        parser.add_argument('-P', '--port')
        parser.add_argument('-u', '--username')
        parser.add_argument('-p', '--password')
        parser.add_argument('-a', '--apikey')
        args = parser.parse_args()
        if args.hostname is not None:
            self.host = args.hostname
        if args.port is not None:
            self.port = args.port
        if args.username is not None:
            self.username = args.username
        if args.password is not None:
            self.password = args.password
        if args.apikey is not None:
            self.apikey = args.apikey

    def extractServerConnectionDetailsFromConfiguration(self, config):
        parser = self.parseAndReadConfigFileIntoMemory(config)

        try:
            self.host = parser.get('server', 'host')
            self.port = parser.get('server', 'port')
            self.username = parser.get('server', 'username')
            self.password = parser.get('server', 'password')
            self.apikey = parser.get('server', 'apikey')

        except:
            self.displayConfigurationFileFormatInstructions(config)
            raise

    def parseAndReadConfigFileIntoMemory(self, config):
        parser = ConfigParser()
        try:
            config_file = open(config)
            parser.readfp(config_file)
            config_file.close()

        except IOError:
            sys.stderr.write('Unable to open ' + config + '\n')
        return parser

    def displayConfigurationFileFormatInstructions(self, config):
        sys.stderr.write('Unable to parse ' + config + '\n')
        sys.stderr.write('Format should be:\n')
        sys.stderr.write('[server]\n')
        sys.stderr.write('host = <sabnzbd server>\n')
        sys.stderr.write('port = <sabnzbd port>\n')
        sys.stderr.write('username = <sabnzbd name> | None\n')
        sys.stderr.write('password = <sabnzbd password> | None\n')
        sys.stderr.write('apikey = <sabnzbd apikey> | None\n')