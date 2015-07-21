#!/usr/bin/python3
import urwid
import utils

class FileLine(urwid.Text):
    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

class FileViewer(urwid.ListBox):
    signals = ['quit']

    def __init__(self):
        self.body = []
        self.walker = urwid.SimpleFocusListWalker(self.body)
        super(FileViewer, self).__init__(self.walker)

    def show_file(self, path, line):
        self.walker.clear()

        i = 1
        for line_content in utils.read_file(path):
            self.walker.append(urwid.AttrMap(FileLine("{0} : {1}".format(str(i), line_content[0:-1])), None, focus_map='reversed'))
            i += 1
                
        self.set_focus(line - 1)
        self.set_focus_valign('middle')

    def keypress(self, size, key):
        if key == 'j':
            key = 'down'
        elif key == 'k':
            key = 'up'
        
        if key == 'q':
            urwid.emit_signal(self, 'quit')
            return True
        if key == 'up' and self.focus_position == 0:
            return None
        
        return super(FileViewer, self).keypress(size, key)

