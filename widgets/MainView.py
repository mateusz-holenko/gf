#!/usr/bin/python3
import urwid
import controller
import subprocess
from widgets.FileViewer import FileViewer
from widgets.CustomListBox import CustomListBox

class EditBox(urwid.Filler):
    def on_enter(self, text):
        pass

    def on_cancel(self):
        pass

    def keypress(self, size, key): 
        if key == 'enter':
            self.on_enter(self.original_widget.edit_text)
            return None
        elif key == 'esc':
            self.on_cancel()
            return None
        
        super(EditBox, self).keypress(size, key)

class StatusLine(urwid.Pile):
    def __init__(self, markup):
        self.text = urwid.Text(markup)
        self._action = None
        super(StatusLine, self).__init__([self.text])

    def set_text(self, text):
        self.text.set_text(text)

    def ask_and_run(self, text, action):
        self._action = action
        edit = EditBox(urwid.Edit(text))
        edit.on_enter = self._on_enter
        edit.on_cancel = self._close_edit
        self.contents.append((edit, ('given', 1)))
        self.focus_position = 1

    def _on_enter(self, text):
        if self._action:
            self._action(text)
        self._action = None
        self._close_edit()

    def _close_edit(self):
        del(self.contents[1])
        controller.main_view.focus_position = 'body'

class MainView(urwid.Frame):
    def __init__(self):
        self.file_viewer = None
        self.results_list = CustomListBox(controller.result_walker)
        self.status_line = StatusLine('')
        controller.result_walker.set_focus_changed_callback(self._focus_changed)
        urwid.connect_signal(self.results_list, 'show', self.show_file_view)
        urwid.connect_signal(self.results_list, 'edit', self.open_editor)
        super(MainView, self).__init__(self.results_list, header=urwid.Text('GF improved 0.1'), footer=self.status_line)

    def open_editor(self):
        for result in controller.selected_results:
            subprocess.call(["vim", "+" + str(result.line_number), result.path])
        controller.deselect_all_results()
        self._invalidate()

    def show_file_view(self, result):
        self.file_viewer = FileViewer()
        urwid.connect_signal(self.file_viewer, 'quit', self.hide_file_view)
        self.file_viewer.show_file(result.path, result.line_number)

        self.body = urwid.Pile([self.results_list, self.file_viewer])
        self.body.focus_position = 1

    def hide_file_view(self):
        self.body = self.results_list
        self.file_viewer = None

    def keypress(self, size, key):
        if key == 'tab' and self.file_viewer:
            self.body.focus_position = (self.body.focus_position + 1) % 2
            return None
        if key == 'f' and self.focus_position == 'body':
            self.focus_position = 'footer'
            self.status_line.ask_and_run('Filter: ', self._do_filtering)
            return None

        return super(MainView, self).keypress(size, key)

    def refresh_status(self):
        self._focus_changed(self.results_list.focus_position)

    def _focus_changed(self, position):
        self.status_line.set_text("Position: " + str(position + 1) + " / " + str(len(self.results_list.body)))

    def _do_filtering(self, text):
        controller.filter(text)

