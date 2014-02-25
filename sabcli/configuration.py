import sys
from ConfigParser import ConfigParser, NoSectionError, NoOptionError

class configuration():
    def __init__(self, config):
        self.extractServerConnectionDetailsFromConfiguration(config)

    def extractServerConnectionDetailsFromConfiguration(self, config):
        parser = self.parseAndReadConfigFileIntoMemory(config)

        try:
            self.host = parser.get('server', 'host')
            self.port = parser.get('server', 'port')
            self.username = parser.get('server', 'username')
            self.password = parser.get('server', 'password')
            self.apikey = parser.get('server', 'apikey')

        except (NoSectionError, NoOptionError):
            self.displayConfigurationFormatHelpInstructions(config)
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

    def displayConfigurationFormatHelpInstructions(self, config):
        sys.stderr.write('Unable to parse ' + config + '\n')
        sys.stderr.write('Format should be:\n')
        sys.stderr.write('[server]\n')
        sys.stderr.write('host = <sabnzbd server>\n')
        sys.stderr.write('port = <sabnzbd port>\n')
        sys.stderr.write('username = <sabnzbd name> | None\n')
        sys.stderr.write('password = <sabnzbd password> | None\n')
        sys.stderr.write('apikey = <sabnzbd apikey> | None\n')