import sys
import curses

class sabScrollPresenter( object ):

    def __init__(self):
        self.index = []
        self.view = 0

        self.scroll = {"totallines":0,
                       "firstline":0,
                       "lastline":0}

        self.window = sys.modules["__main__"].window

    def display(self):
        self.print_scroll()

    def print_scroll(self):
        if self.index:
            while self.index[self.view] > self.indexCount[self.view]:
                self.index[self.view] -= 1
            index = self.index[self.view]
        else :
            index = -1
'''
        # Redraw * in front of selected item.
        if index == -1:
            self.scroll['firstline'] = 0

        if len(self.scroll['item']) > 0:
            # removing *
            if self.scroll['lastitem'] > -1 and self.scroll['lastitem'] < len(self.scroll['item']):
                for i in self.scroll['item'][self.scroll['lastitem']]:
                    self.pad.addstr(i, 0, ' ')

            if index > -1:
                for i in self.scroll['item'][index]:
                    if i > -1:
                        if self.details['move'] == None:
                            self.pad.addstr(i, 0, '*')
                        else:
                            self.pad.addstr(i, 0, '*', curses.color_pair(2))
                        self.scroll['firstline'] = self.scroll['item'][index][0]
                        self.scroll['lastitem'] = index

        if self.scroll['totallines'] >= int(self.size[0])-1:
            if self.scroll['totallines']-int(self.size[0]) <= 0:
                self.scroll['totallines'] = self.scroll['totallines'] + 1

            i = 0
            temp = -1
            while i < int(self.size[0])-5 :
                percentage = self.scroll['firstline'] * 100 / (self.scroll['totallines']-2)
                pct = i * 100 / ( int(self.size[0]) - 7 )

                if percentage < 5: percentage = 4

                if temp == -1:
                    if pct > percentage - 5 and pct < percentage + 5:
                        temp = 3

                    if temp > 0:
                        self.stdscr.addstr(i+4, int(self.size[1])-1, '#')
                        temp = temp -1
                    else:
                        self.stdscr.addstr(i+4, int(self.size[1])-1, '|')

                    i += 1

            # If total lines is less than the size of the window, then show the entire window, always.
            if self.scroll['totallines'] < int(self.size[0])-3:
                    self.scroll['firstline'] = 0

            # If firstline is less than halfway down the screen, print everything.
            if self.scroll['firstline'] < (int(self.size[0]))/2:
                    self.scroll['firstline'] = 0

        # Makes sure there are no empty lines in the bottom of the screen.
        elif self.scroll['firstline']-(self.scroll['totallines']-int(self.size[0])) > (int(self.size[0]))/2:
            self.scroll['firstline'] = self.scroll['totallines'] - int(self.size[0])+4
        else:
            self.scroll['firstline'] -= (int(self.size[0])-7)/2
            '''