import sys, time

class sabStatusController():

    def __init__(self):
        self.statusPresenter = sys.modules["__main__"].statusPresenter
        self.status = {}

    def update(self, state = {}):
        self.status = state
        self.status["updated"] = '[Updated: ' + time.strftime("%H:%M:%S", time.localtime(state['last_fetch_time'])) + '] '

        if 'total_size' in state:
            # History view
            self.status["stats"] = str('[Transfered: %s / %s / %s]' % ( state['total_size'], state['month_size'], state['week_size']))
        else:
            # Queue view or pre 0.5.2 view
            self.status["stats"] = str('[Queue: %.2f / %.2f GB (%2.0f%%)] [Up: %s]' %\
                            ( ( float(state['mb']) - float(state['mbleft']) ) / 1024
                              , float(state['mb']) / 1024
                              , 100 * ( float(state['mb']) - float(state['mbleft'])) / (float(state['mb'])+0.01)
                              , state['uptime']))

        self.status["diskusage"] = '[Disk: %.2f / %.2f GB]' % ( float(state['diskspace2']), float(state['diskspacetotal2']))

    def display(self):
        self.statusPresenter.display(self.status)