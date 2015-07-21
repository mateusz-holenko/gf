#!/usr/bin/python3
import urwid
import controller
import subprocess
from widgets.FileViewer import FileViewer
from widgets.CustomListBox import CustomListBox

class MainView(urwid.Frame):
    def __init__(self):
        self.file_viewer = None
        self.results_list = CustomListBox(controller.result_walker)
        urwid.connect_signal(self.results_list, 'show', self.show_file_view)
        urwid.connect_signal(self.results_list, 'edit', self.open_editor)
        super(MainView, self).__init__(self.results_list, header=urwid.Text('GF improved 0.1'))

    def open_editor(self, path, line):
        subprocess.call(["vim", "+" + str(line), path])
        self._invalidate()

    def show_file_view(self, path, line):
        self.file_viewer = FileViewer()
        urwid.connect_signal(self.file_viewer, 'quit', self.hide_file_view)
        self.file_viewer.show_file(path, line)

        self.body = urwid.Pile([self.results_list, self.file_viewer])
        self.body.focus_position = 1

    def hide_file_view(self):
        self.body = self.results_list
        self.file_viewer = None

    def keypress(self, size, key):
        if key == 'tab' and self.file_viewer:
            self.body.focus_position = (self.body.focus_position + 1) % 2
            return True

        return super(MainView, self).keypress(size, key)
