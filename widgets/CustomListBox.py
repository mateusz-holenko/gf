#!/usr/bin/python3
import urwid
import controller

class CustomListBox(urwid.ListBox):

    def __init__(self, body):
        super(CustomListBox, self).__init__(body)

    def focus_next(self):
        if self.focus_position < len(self.body) - 1:
            self.set_focus(self.focus_position + 1, 'above')
            self._invalidate()

    def focus_prev(self):
        if self.focus_position > 0:
            self.set_focus(self.focus_position - 1, 'below')
            self._invalidate()

    def focus_top(self):
        self.set_focus(0)
        self._invalidate()

    def focus_bottom(self):
        self.set_focus(len(self.body) - 1)
        self._invalidate()
