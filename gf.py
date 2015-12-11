#!/usr/bin/python3
import sys
import urwid
import logging
import controller
import shortcut_manager
from widgets.MainView import MainView

import concurrent.futures

directory = '.'
expr = sys.argv[1]

shortcut_manager.push_mode('list')
controller.main_view = MainView()
controller.scan(directory)
controller.grep(expr)
controller.main_loop = urwid.MainLoop(controller.main_view, palette=[('reversed', 'standout', ''), ('matched', 'dark red', '')])

controller.main_loop.run()
