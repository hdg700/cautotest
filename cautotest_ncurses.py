# -*- coding: utf-8 -*-


import curses


def init_curses():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)

def restore():
    curses.nocbreak()
    curses.echo()
    curses.endwin()

class LineItem(object):
    """LineItem class represents one list line"""
    def __init__(self, project, code_dir, tests_dir, active=True):
        self.project = project
        self.code_dir = code_dir
        self.tests_dir = tests_dir
        self.active = active

    def draw(self, scr, row, col, selected):
        if selected:
            help_text = u' (\'d\' - delete, \'e\' - edit)'
        else:
            help_text = u' ' * 100
        scr.addstr(row, col, '[' + self.project + ']' + help_text,
                curses.color_pair(2) if selected else curses.color_pair(1))
        row += 1
        scr.addstr(row, col+2, self.code_dir, curses.color_pair(1))
        row += 1
        scr.addstr(row, col+2, self.tests_dir, curses.color_pair(1))
        return row+1


class AutotestConsole(object):
    """Autotest daemon console client for managing projects"""

    def __init__(self):
        self.items = []
        self.init_items()
        self.current_item = 0

        self.scr = curses.initscr()
        init_curses()
        self.scr.border(0)
        self.scr.keypad(1)

    def init_items(self):
        self.items.append(LineItem('spravka',
                '/home/hdgasdfasdfasdf;laksdfj;askljdf700/work/spravka/application',
                '/home/hdg700/work/spravka/tests'))
        self.items.append(LineItem('amurnews',
                '/home/hdg700/work/amurnews/application',
                '/home/hdg700/work/amurnews/tests'))
        self.items.append(LineItem('total',
                '/home/hdg700/work/total/application',
                '/home/hdg700/work/total/tests'))

    def draw(self):
        self.scr.addstr(1, 2, u'AutotestDaemon Console Client')
        next_row = 3
        for i, item in enumerate(self.items):
            next_row = item.draw(self.scr, next_row, 3, i == self.current_item) + 1
        self.scr.refresh()

    def loop(self):
        self.draw()
        while True:
            try:
                c = self.scr.getch()
            except:
                break
            if c in (curses.KEY_DOWN, ord('j')):
                self.current_item = (self.current_item + 1) % len(self.items)
            elif c in (curses.KEY_UP, ord('k')):
                self.current_item = (self.current_item - 1) % len(self.items)
            self.draw()
        restore()


if __name__ == "__main__":
    try:
        ob = AutotestConsole()
        ob.loop()
    except Exception as e:
        restore()
        print e
