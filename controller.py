#!/usr/bin/python3
import re
import utils
import urwid
import filemanager
from widgets.ListBoxItem import ListBoxItem

interesting_files = []
result_walker = None
selected_files = []

class SearchResult:
    def __init__(self, path, line_content, line_number, match_location):
        self.path = path
        self.line_content = line_content
        self.line_number = line_number
        self.match_location = match_location

def _parse_file(file, pattern):
    results = []
    line_number = 1
    lines = utils.read_file(file)
    if lines is None:
        return None
    for line in lines:
        line = line[:-1]
        m = list(pattern.finditer(line))
        if any(m):
            results.append(SearchResult(file, line, line_number, m[0].span()))
        line_number += 1
    return results

def scan(directory):
    global interesting_files
    interesting_files = filemanager.scan(directory)

def grep(expr):
    global result_walker

    results = []
    pattern = re.compile(expr)
    for file in interesting_files:
        parsed = _parse_file(file, pattern)
        if parsed is not None:
            results.extend(parsed)
        else:
            print("Skipping file: " + file)

    items = []
    counter = 1
    for result in results:
        item = ListBoxItem(counter, result.path, result.line_number, result.line_content, result.match_location)
        items.append(urwid.AttrMap(item, None, focus_map='reversed'))
        counter += 1
    result_walker = urwid.SimpleFocusListWalker(items)

    return results

