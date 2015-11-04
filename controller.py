#!/usr/bin/python3
import re
import utils
import urwid
import filemanager
from widgets.ListBoxItem import ListBoxItem

interesting_files = []
result_walker = urwid.SimpleFocusListWalker([])
selected_results = []
grep_result = []
dic = {}

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
    global grep_result

    grep_result = []
    pattern = re.compile(expr)
    for file in interesting_files:
        parsed = _parse_file(file, pattern)
        if parsed is not None:
            grep_result.extend(parsed)
        else:
            print("Skipping file: " + file)

    reset_filter()

def reset_filter():
    result_walker.clear()
    dic.clear()

    counter = 1
    for result in grep_result:
        item = ListBoxItem(counter, result)
        dic[result] = item
        result_walker.append(urwid.AttrMap(item, None, focus_map='reversed'))
        counter += 1

def toggle_result(result):
    global selected_results

    is_selected = result in selected_results
    select_result(result, not is_selected)

def select_result(result, is_selected):
    global selected_results

    #todo: optimize
    if is_selected:
        if result not in selected_results: 
            selected_results.append(result)
            dic[result].set_selected(True)
    else:
        if result in selected_results: 
            selected_results.remove(result)
            dic[result].set_selected(False)

def deselect_all_results():
    for result in selected_results:
        dic[result].set_selected(False)
    selected_results.clear()

