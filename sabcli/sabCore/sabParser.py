import xml.etree.ElementTree as ElementTree
import xmltodict

class sabParser():

    def convertSABXMLtoDictionary(self, xml = ""):
        ''' Convert status object to python dictionary '''
        return xmltodict.parse(xml)

    def fixBrokenXML(self, command, status_obj):
        # Fix broken xml from sabnzbd
        if command == 'warnings':
            status_obj = status_obj.replace("<warnings>", "<root>\n<warnings>")
            status_obj = status_obj.replace("</warnings>", "</warnings></root>")
        if command == 'details':
            status_obj = status_obj.replace("<files>", "<root>\n<files>")
            status_obj = status_obj.replace("</files>", "</files></root>")
        return status_obj

    def parseStatus(self, command, status_obj):
        ''' Convert web output to boolean value '''

        if not status_obj:
            return False

        if self.retval == 'ok' :
            return True
        if self.retval.find('error') == 0 :
            return False

        if command == 'priority':
            self.index[self.view] = int(self.retval)

        if command in ('version', 'move', 'priority', 'newapikey', 'addlocalfile', 'addurl', 'addid'):
            return self.retval

        status_obj = self.fixBrokenXML(command, status_obj)

        try:
            status_obj = status_obj.replace('&', '&amp;')
            root = ElementTree.XML(status_obj.strip())
            self.return_data = self.convertSABXMLtoDictionary(root)
            self.command_status = 'ok'

        except ValueError:
            self.command_status = 'error'
            return False
        return True
