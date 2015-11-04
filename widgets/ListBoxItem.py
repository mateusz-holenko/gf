#!/usr/bin/python3
import urwid
import logging
import controller
import subprocess

logger = logging.getLogger(__name__)

class ListBoxItem(urwid.Columns):
    FILEPATH_LEN = 45

    def __init__(self, id, result):
        self.id = id
        self.result = result

        path = result.path
        if len(path) > ListBoxItem.FILEPATH_LEN:
            path = "..." + path[(-ListBoxItem.FILEPATH_LEN + 3):]
        text = [result.line_content[0:result.match_location[0]], ('matched', result.line_content[result.match_location[0]:result.match_location[1]]), result.line_content[result.match_location[1]:]]
        super(ListBoxItem, self).__init__([
            ('fixed', 5, urwid.Text(str(id))),
            ('fixed', ListBoxItem.FILEPATH_LEN, urwid.Text(path)),
            ('fixed', 5, urwid.Text(str(result.line_number))),
            urwid.Text(text, wrap='clip')], dividechars=1)

    def set_selected(self, is_selected):
        self.contents[0][0].set_text(str(self.id) + "*" if is_selected else str(self.id))

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

