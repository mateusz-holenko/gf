#!/usr/bin/python3
import urwid
import logging
import controller
from widgets.FileViewer import FileViewer

logger = logging.getLogger(__name__)
file_viewer = FileViewer()

class CustomListBox(urwid.ListBox):
    # _metaclass_ = urwid.signals.MetaSignals
    signals = ['show', 'edit']

    def __init__(self, body):
        super(CustomListBox, self).__init__(body)

    def keypress(self, size, key):
        if key == 'j':
            key = 'down'
        elif key == 'k':
            key = 'up'
        elif key == 'enter':
            urwid.emit_signal(self, 'show', self.focus.original_widget.path, self.focus.original_widget.line_number)
            return None
        elif key == 'e':
            if len(controller.selected_files) == 0:
                self.focus.original_widget.set_selected(True)
            urwid.emit_signal(self, 'edit')
            return None
        elif key == 't':
            self.focus.original_widget.toggle_selected()
            return None

        if key == 'down' and self.focus_position == len(self.body) - 1:
            return None

        return super(CustomListBox, self).keypress(size, key)

    def deselect_all(self):
        for element in self.body:
            element.original_widget.set_selected(False)
