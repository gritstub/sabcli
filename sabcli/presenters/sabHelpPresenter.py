from cursesUI.cursesWindow import cursesWindow


class sabHelpPresenter:
    def __init__(self, window = None):
        if not window:
            window = cursesWindow()
        self.window = window

        self.screen = []
        self.pad = []

    def display(self):
        self.screen = []
        self.pad = []

        self.displayGeneralInformation()
        self.displayNavigationInformation()

        self.displayQueueViewInformation()

        self.window.draw(self.screen)
        self.window.pad.draw(self.pad)

    def displayGeneralInformation(self):
        self.screen.append((3, 2, 'Keymap:\n', ''))
        self.screen.append((0, 3, '-' * int(self.window.size[1]) + '\n', ''))

    def displayNavigationInformation(self):
        self.pad.append((3, 1,  '|' + '-' * 46 + '|' + '\n', ''))
        self.pad.append((3, 2,  '| General and Navigation                       |\n', ''))
        self.pad.append((3, 3,  '|' + '-' * 46 + '|' + '\n', ''))
        self.pad.append((3, 4,  '| 1              Queue screen                  |\n', ''))
        self.pad.append((3, 5,  '| 2              History screen                |\n', ''))
        self.pad.append((3, 6,  '| 3              Warnings screen               |\n', ''))
        self.pad.append((3, 7,  '| 4              More screen                   |\n', ''))
        self.pad.append((3, 8,  '| 5/?            Help screen                   |\n', ''))
        self.pad.append((3, 9,  '| Q/q            Quit                          |\n', ''))
        self.pad.append((3, 10, '| S              Shutdown                      |\n', ''))
        self.pad.append((3, 11, '| R              Restart                       |\n', ''))
        self.pad.append((3, 12, '| Up/Down        Select item/setting           |\n', ''))
        self.pad.append((3, 13, '| PageUp/Down    Select item (jump 5)          |\n', ''))
        self.pad.append((3, 14, '| Home/End       Jump to first or last item    |\n', ''))
        self.pad.append((3, 15, '| Enter          Access/Apply changes          |\n', ''))
        self.pad.append((3, 16, '| Del/Backspace  Delete (all* or selected)     |\n', ''))
        self.pad.append((3, 17, '|                *only on history screen       |\n', ''))
        self.pad.append((3, 18, '|' + '-' * 46 + '|' + '\n', ''))

    def displayQueueViewInformation(self):
        self.pad.append((53, 1, '|' + '-' * 45 + '|' + '\n', ''))
        self.pad.append((53, 2, '| Queue view                                  |\n', ''))
        self.pad.append((53, 3, '|' + '-' * 45 + '|' + '\n', ''))
        self.pad.append((53, 4, '| Left/Right  Access settings                 |\n', ''))
        self.pad.append((53, 5, '| m           Move (select and place)         |\n', ''))
        self.pad.append((53, 6, '| r           Resume (all or selected)        |\n', ''))
        self.pad.append((53, 7, '| p           Pause (all or selected)         |\n', ''))
        self.pad.append((53, 8, '| d           Enter/Exit details view         |\n', ''))
        self.pad.append((53, 9, '|' + '-' * 45 + '|' + '\n', ''))