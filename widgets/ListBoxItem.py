#!/usr/bin/python3
import urwid
import logging
import controller
import subprocess

logger = logging.getLogger(__name__)

class ListBoxItem(urwid.Columns):
    FILEPATH_LEN = 45

    def __init__(self, id, path, line_number, line_content, match_span):
        self.path = path
        self.line_number = line_number
        self.id = id
        self.is_selected = False
        if len(path) > ListBoxItem.FILEPATH_LEN:
            path = "..." + path[(-ListBoxItem.FILEPATH_LEN + 3):]
        text = [line_content[0:match_span[0]], ('matched', line_content[match_span[0]:match_span[1]]), line_content[match_span[1]:]]
        super(ListBoxItem, self).__init__([
            ('fixed', 5, urwid.Text(str(id))),
            ('fixed', ListBoxItem.FILEPATH_LEN, urwid.Text(path)),
            ('fixed', 5, urwid.Text(str(line_number))),
            urwid.Text(text, wrap='clip')], dividechars=1)

    def toggle_selected(self):
        self.is_selected = not self.is_selected
        self.set_selected(self.is_selected)

    def set_selected(self, is_selected):
        self.contents[0][0].set_text(str(self.id) + "*" if is_selected else str(self.id))
        tuple = (self.path, self.line_number)
        if is_selected:
            if tuple not in controller.selected_files: controller.selected_files.append(tuple)
        else:
            if tuple in controller.selected_files: controller.selected_files.remove(tuple)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

