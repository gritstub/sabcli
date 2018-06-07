from cursesUI.cursesWindow import cursesWindow
from presenters.sabScrollPresenter import sabScrollPresenter


class sabDownloadDetailsPresenter():
    def __init__(self, window = None, scrollPresenter = None):
        self.displayFileInformation = None
        if not window:
            window = cursesWindow()
        self.window = window

        if not scrollPresenter:
            scrollPresenter = sabScrollPresenter()
        self.scrollPresenter = scrollPresenter

        self.screen = []
        self.pad = []

    def display(self, state):
        self.screen = []
        self.pad = []

        self.displayGeneralInformation()
        self.displayDownloadDetails(state)

        self.window.draw(self.screen)
        self.window.pad.draw(self.pad)

        state["item_size"] = 3
        self.scrollPresenter.display(state)

    def displayGeneralInformation(self):
        self.screen.append((3, 2, "# - Filename:\n", ""))
        self.screen.append((0, 3, "-" * int(self.window.size[1] + "\n"), ""))

    def displayDownloadDetails(self, state):
        if "files" not in state:
            return

        for file_detail in state["files"]:
            self.displayDownloadFileInformation(file_detail)

    def displayDownloadFileInformation(self, file_detail):
        status_color = ''
        if file_detail['status'] != "finished":
            status_color = 2

        self.pad.append((' ' * 3, ''))
        self.pad.append((str(file_detail['nzf_id']), 3))
        self.pad.append((" - ", ""))

        self.pad.append((file_detail['filename'] + '\n', ''))

        self.pad.append(("       [Status: ", ''))
        self.pad.append((file_detail['status'], status_color))

        self.pad.append(("] [Age: ", ''))
        self.pad.append((file_detail['age'], status_color))

        self.pad.append(("] [Downloaded: ", ''))
        self.pad.append((str(float(file_detail['mb']) - float(file_detail['mbleft'])), status_color))
        self.pad.append(("/%s MB]\n\n" % float(file_detail['mb']), ''))