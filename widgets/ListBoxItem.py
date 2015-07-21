#!/usr/bin/python3
import urwid
import logging
import subprocess

logger = logging.getLogger(__name__)

class ListBoxItem(urwid.Columns):
    FILEPATH_LEN = 45

    def __init__(self, id, path, line_number, line_content, match_span):
        self.path = path
        self.line_number = line_number
        if len(path) > ListBoxItem.FILEPATH_LEN:
            path = "..." + path[(-ListBoxItem.FILEPATH_LEN + 3):]
        text = [line_content[0:match_span[0]], ('matched', line_content[match_span[0]:match_span[1]]), line_content[match_span[1]:]]
        super(ListBoxItem, self).__init__([
            ('fixed', 5, urwid.Text(str(id))),
            ('fixed', ListBoxItem.FILEPATH_LEN, urwid.Text(path)),
            ('fixed', 5, urwid.Text(str(line_number))),
            urwid.Text(text, wrap='clip')], dividechars=1)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

