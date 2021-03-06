#!/usr/bin/python3
import urwid
import controller
import subprocess
import shortcut_manager
from widgets.FileViewer import FileViewer
from widgets.ResultsViewer import ResultsViewer

class EditBox(urwid.Filler):
    signals = [ 'entered', 'canceled' ]

    def set_text(self, text):
        self.original_widget.set_caption(text)

    def keypress(self, size, key):
        if key == 'enter':
            urwid.emit_signal(self, 'entered', self.original_widget.edit_text)
            self.original_widget.set_edit_text('')
        elif key == 'esc':
            urwid.emit_signal(self, 'canceled', '')
            self.original_widget.set_edit_text('')
        else:
            super(EditBox, self).keypress(size, key)
        return None

class StatusCommandWidget(urwid.Pile):

    def __init__(self, markup):
        self.status = urwid.Text(markup)
        self.edit_box = EditBox(urwid.Edit())
        self.right_status = urwid.Text('', align='right')
        urwid.connect_signal(self.edit_box, 'entered', self._hide_command)
        urwid.connect_signal(self.edit_box, 'canceled', self._hide_command)
        super(StatusCommandWidget, self).__init__([self.status, self.right_status])
        self.focus_position = 1

    def set_right_status(self, text):
        self.right_status.set_text(text)

    def ask_and_run(self, text, action):
        self.edit_box.set_text(text)
        urwid.connect_signal(self.edit_box, 'entered', self._call_and_disconnect, user_args=[action])
        self.contents[1] = (self.edit_box, ('given', 1))

    def _call_and_disconnect(self, action, text):
        urwid.disconnect_signal(self.edit_box, 'entered', self._call_and_disconnect, user_args=[action])
        action(text)

    def _hide_command(self, arg):
        self.contents[1] = (urwid.Filler(self.right_status), ('given', 1))

class MainView(urwid.Frame):
    def __init__(self):
        self.file_viewer = None
        self.results_list = ResultsViewer(controller.result_walker)
        self.status_line = StatusCommandWidget('')
        urwid.connect_signal(self.status_line.edit_box, 'entered', self._focus_list)
        urwid.connect_signal(self.status_line.edit_box, 'canceled', self._focus_list)
        controller.result_walker.set_focus_changed_callback(self._focus_changed)
        urwid.connect_signal(controller.result_walker, 'modified', self._results_modified)
        urwid.connect_signal(self.results_list, 'show', self.show_file_view)
        urwid.connect_signal(self.results_list, 'edit', self.open_editor)
        super(MainView, self).__init__(self.results_list, header=urwid.Text('GF improved 0.1'), footer=self.status_line)

        shortcut_manager.register(['g', 'g'], self.results_list.focus_top)
        shortcut_manager.register('G', self.results_list.focus_bottom)
        shortcut_manager.register('t', self.results_list.toggle_focused)
        shortcut_manager.register('T', self.results_list.toggle_all)
        shortcut_manager.register('j', self.results_list.focus_next)
        shortcut_manager.register('k', self.results_list.focus_prev)
        shortcut_manager.register('e', self.results_list.edit_selected)
        shortcut_manager.register(['f', 'f'], self.results_list.filter_focused_file)
        shortcut_manager.register(['f', 'd'], self.results_list.filter_focused_file)
        shortcut_manager.register(['f', 'u'], controller.filter_distinct_files)
        shortcut_manager.register(['f', 'e'], self.results_list.filter_by_extension)
        shortcut_manager.register(['f', 'c'], self._custom_filter)
        shortcut_manager.register('x', controller.reset_filter)
        shortcut_manager.register('enter', self.results_list.show_focused_content)
        shortcut_manager.register('q', controller.exit)

        shortcut_manager.status_changed_callback = self._shortcut_manager_status_changed

    def _shortcut_manager_status_changed(self):
        self.status_line.set_right_status(''.join(shortcut_manager.keys))

    def open_editor(self):
        for result in controller.selected_results:
            subprocess.call(["vim", "+" + str(result.line_number), result.path])
        controller.deselect_all_results()
        self._invalidate()

    def show_file_view(self, result):
        self.file_viewer = FileViewer()

        shortcut_manager.register('q', self.hide_file_view)
        shortcut_manager.register('j', self.file_viewer.focus_next)
        shortcut_manager.register('k', self.file_viewer.focus_prev)
        shortcut_manager.register('J', self.results_list.focus_next)
        shortcut_manager.register('K', self.results_list.focus_prev)
        shortcut_manager.register(['g', 'g'], self.file_viewer.focus_top)
        shortcut_manager.register('G', self.file_viewer.focus_bottom)

        urwid.connect_signal(self.file_viewer, 'quit', self.hide_file_view)
        self.file_viewer.show_file(result.path, result.line_number)

        self.body = urwid.Pile([self.results_list, self.file_viewer])
        self.body.focus_position = 1

    def hide_file_view(self):
        shortcut_manager.register('q', controller.exit)
        shortcut_manager.register(['g', 'g'], self.results_list.focus_top)
        shortcut_manager.register('G', self.results_list.focus_bottom)
        shortcut_manager.register('j', self.results_list.focus_next)
        shortcut_manager.register('k', self.results_list.focus_prev)

        self.body = self.results_list
        self.file_viewer = None

    def keypress(self, size, key):
        if key == 'tab' and self.file_viewer:
            self.body.focus_position = (self.body.focus_position + 1) % 2
            return None
        if self.focus_position == 'body':
            shortcut_manager.handle_key(key)
            return None

        return super(MainView, self).keypress(size, key)

    def _custom_filter(self):
        self.focus_position = 'footer'
        self.status_line.ask_and_run('Filter: ', self._do_filtering)

    def _focus_changed(self, position):
        if position == -1 or len(self.results_list.body) == 0:
            self.status_line.status.set_text("No results found.")
        else:
            self.status_line.status.set_text("Position: " + str(position + 1) + " / " + str(len(self.results_list.body)))

    def _do_filtering(self, text):
        controller.filter(text)

    def _results_modified(self):
        index = -1
        try:
            index = self.results_list.focus_position
        except IndexError:
            pass

        self._focus_changed(index)

    def _focus_list(self, arg):
        self.focus_position = 'body'

