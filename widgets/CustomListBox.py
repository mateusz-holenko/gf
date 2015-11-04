#!/usr/bin/python3
import urwid
import controller

class CustomListBox(urwid.ListBox):
    signals = ['show', 'edit', 'moved']

    def __init__(self, body):
        super(CustomListBox, self).__init__(body)

    def keypress(self, size, key):
        if key == 'j':
            key = 'down'
        elif key == 'k':
            key = 'up'
        elif key == 'enter':
            urwid.emit_signal(self, 'show', self.focus.original_widget.result)
            return None
        elif key == 'e':
            if len(controller.selected_results) == 0:
                controller.select_result(self.focus.original_widget.result, True)
            urwid.emit_signal(self, 'edit')
            return None
        elif key == 't':
            controller.toggle_result(self.focus.original_widget.result)
            return None
        elif key == 'T':
            for element in self.body:
                controller.toggle_result(element.original_widget.result)
            return None
        elif key == 'd':
            controller.filter_distinct_files()
            return None
        elif key == 'x':
            controller.reset_filter()
            return None

        if key == 'down' and self.focus_position == len(self.body) - 1:
            return None

        if key == 'up' or key == 'down':
            urwid.emit_signal(self, 'moved', self.focus_position)

        return super(CustomListBox, self).keypress(size, key)

