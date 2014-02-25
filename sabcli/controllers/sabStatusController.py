import sys

class sabStatusController():

    def __init__(self):
        self.statusPresenter = sys.modules["__main__"].statusPresenter
        self.status = {}

    def update(self, state = {}):
        self.status["updated"] = '[Updated: ' + time.strftime("%H:%M:%S", time.localtime(state['last_fetch_time'])) + '] '

        if 'total_size' in state:
            # History view
            self.status["stats"] = str('[Transfered: %s / %s / %s]' % ( rd['total_size'], rd['month_size'], rd['week_size']))
        else:
            # Queue view or pre 0.5.2 view
            self.status["stats"] = str('[Queue: %.2f / %.2f GB (%2.0f%%)] [Up: %s]' %\
                            ( ( float(rd['mb']) - float(rd['mbleft']) ) / 1024
                              , float(rd['mb']) / 1024
                              , 100 * ( float(rd['mb']) - float(rd['mbleft'])) / (float(rd['mb'])+0.01)
                              , rd['uptime']))

        self.status["diskusage"] = '[Disk: %.2f / %.2f GB]' % ( float(rd['diskspace2']), float(rd['diskspacetotal2']))

    def display(self):
        self.statusPresenter.display(self.status)