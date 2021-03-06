#!/usr/bin/python3
import os.path
import sys
import re
import utils
import urwid
import filemanager
from widgets.MainView import MainView
from widgets.ListBoxItem import ListBoxItem

main_view = None
main_loop = None

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

    def matches(self, pattern):
        return pattern.search(self.path) is not None or pattern.search(self.line_content) is not None

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

def exit():
    raise urwid.ExitMainLoop()

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

def search(expr, location, direction):
    if location >= len(result_walker) or location < 0:
        raise Excepion

    #todo: optimize
    pattern = re.compile(expr)
    if direction == 'down':
        for index in range(location, len(result_walker)).extend(range(0, location - 1)):
            if result_walker[index].matches(pattern):
                return index
    else:
        for index in range(location, 0).extend(range(len(result_walker) - 1, location)):
            if result_walker[index].matches(pattern):
                return index

    return -1

def filter(expr):
    pattern = re.compile(expr)
    remove_list = []
    for item in result_walker:
        if not item.original_widget.result.matches(pattern):
            remove_list.append(item)

    for remove_item in remove_list:
        result_walker.remove(remove_item)

def filter_distinct_files():
    encountered_files = []
    remove_list = []
    for item in result_walker:
        if item.original_widget.result.path not in encountered_files:
            encountered_files.append(item.original_widget.result.path)
        else:
            remove_list.append(item)

    for remove_item in remove_list:
        result_walker.remove(remove_item)

def filter_file(file):
    remove_list = []
    for item in result_walker:
        if item.original_widget.result.path != file:
            remove_list.append(item)

    for remove_item in remove_list:
        result_walker.remove(remove_item)

def filter_directory(file):
    dir = os.path.dirname(file)
    remove_list = []
    for item in result_walker:
        if os.path.dirname(item.original_widget.result.path) != dir:
            remove_list.append(item)

    for remove_item in remove_list:
        result_walker.remove(remove_item)

def filter_by_extension(file):
    ext = os.path.splitext(file)[1]
    remove_list = []
    for item in result_walker:
        if os.path.splitext(item.original_widget.result.path)[1] != ext:
            remove_list.append(item)

    for remove_item in remove_list:
        result_walker.remove(remove_item)

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

