#!/usr/bin/python3
import urwid
import controller
from widgets.CustomListBox import CustomListBox

class ResultsViewer(CustomListBox):
    signals = ['show', 'edit', 'moved']

    def filter_by_extension(self):
        controller.filter_by_extension(self.focus.original_widget.result.path)

    def filter_focused_file(self):
        controller.filter_file(self.focus.original_widget.result.path)

    def filter_focused_directory(self):
        controller.filter_directory(self.focus.original_widget.result.path)

    def toggle_focused(self):
        controller.toggle_result(self.focus.original_widget.result)
        if self.focus_position < len(self.body) - 1:
            self.focus_position += 1

    def toggle_all(self):
        for element in self.body:
            controller.toggle_result(element.original_widget.result)

    def edit_selected(self):
        if len(controller.selected_results) == 0:
            controller.select_result(self.focus.original_widget.result, True)
        urwid.emit_signal(self, 'edit')

    def show_focused_content(self):
        urwid.emit_signal(self, 'show', self.focus.original_widget.result)


