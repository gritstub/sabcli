import urllib2
from configuration import configuration


class sabChannel():
    def __init__(self, settings = None):
        if not settings:
            settings = configuration()
        self.settings = settings

        self.postdata = None
        self.header = { 'User-Agent' : 'SabnzbdAutomation' }

        if self.settings.username and self.settings.password:
            self.postdata = 'ma_password=' + self.settings.password + '&' +\
                            'ma_username=' + self.settings.username
            self.header['Content-type'] = 'application/x-www-form-urlencoded'

    def requestData(self, path):
        result = self._send(path)
        return result

    def sendCommand(self, path):
        result = self._send(path)
        return result

    def _send(self, path):
        request = urllib2.Request(path, self.postdata, self.header)

        response = urllib2.urlopen(request)
        result = response.read()

        return result