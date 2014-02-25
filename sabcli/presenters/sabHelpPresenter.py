import sys

class sabHelpPresenter( object ):

    def __init__(self):
        self.window = sys.modules["__main__"].window

    def displayGeneralInformation(self):
        self.window.pad.addString(1,3,  '|' + '-' * 46 + '|' + '\n')
        self.window.pad.addString(2,3,  '| General and Navigation                       |\n')
        self.window.pad.addString(3,3,  '|' + '-' * 46 + '|' + '\n')
        self.window.pad.addString(4,3,  '| 1              Queue screen                  |\n')
        self.window.pad.addString(5,3,  '| 2              History screen                |\n')
        self.window.pad.addString(6,3,  '| 3              Warnings screen               |\n')
        self.window.pad.addString(7,3,  '| 4              More screen                   |\n')
        self.window.pad.addString(8,3,  '| 5/?            Help screen                   |\n')
        self.window.pad.addString(9,3,  '| Q              Quit                          |\n')
        self.window.pad.addString(10,3, '| S              Shutdown                      |\n')
        self.window.pad.addString(11,3, '| R              Restart                       |\n')
        self.window.pad.addString(12,3, '| Up/Down        Select item/setting           |\n')
        self.window.pad.addString(13,3, '| PageUp/Down    Select item (jump 5)          |\n')
        self.window.pad.addString(14,3, '| Home/End       Jump to first or last item    |\n')
        self.window.pad.addString(15,3, '| Enter          Access/Apply changes          |\n')
        self.window.pad.addString(16,3, '| Del/Backspace  Delete (all* or selected)     |\n')
        self.window.pad.addString(17,3, '|                *only on history screen       |\n')
        self.window.pad.addString(18,3, '|' + '-' * 46 + '|' + '\n')

    def displayQueueViewInformation(self):
        self.window.pad.addString(1, 53, '|' + '-' * 45 + '|' + '\n')
        self.window.pad.addString(2, 53, '| Queue view                                  |\n')
        self.window.pad.addString(3, 53, '|' + '-' * 45 + '|' + '\n')
        self.window.pad.addString(4, 53, '| Left/Right  Access settings                 |\n')
        self.window.pad.addString(5, 53, '| m           Move (select and place)         |\n')
        self.window.pad.addString(6, 53, '| r           Resume (all or selected)        |\n')
        self.window.pad.addString(7, 53, '| p           Pause (all or selected)         |\n')
        self.window.pad.addString(8, 53, '| d           Enter/Exit details view         |\n')
        self.window.pad.addString(9, 53, '|' + '-' * 45 + '|' + '\n')

    def display(self):
        self.window.addString(2, 3, 'Keymap:\n')
        self.window.addString(3, 0, '-' * int(self.window.size[1] + '\n'))

        self.window.pad.addStr('\n')
        self.displayGeneralInformation()
        self.window.pad.addStr('\n')
        self.displayQueueViewInformation()