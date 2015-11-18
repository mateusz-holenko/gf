#!/usr/bin/python3
import urwid
import utils
from widgets.CustomListBox import CustomListBox

class FileLine(urwid.Text):
    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

class FileViewer(urwid.Frame):
    signals = ['quit']

    def __init__(self):
        self.body = []
        self.walker = urwid.SimpleFocusListWalker(self.body)
        self.content = CustomListBox(self.walker)
        super(FileViewer, self).__init__(self.content, header=urwid.Divider('-'))

    def show_file(self, path, line):
        self.walker.clear()

        i = 1
        for line_content in utils.read_file(path):
            self.walker.append(urwid.AttrMap(FileLine("{0} : {1}".format(str(i), line_content[0:-1])), None, focus_map='reversed'))
            i += 1

        self.content.set_focus(line - 1)
        self.content.set_focus_valign('middle')

