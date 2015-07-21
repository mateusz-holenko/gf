#!/usr/bin/python3
import sys
import urwid
import logging
import controller
from widgets.MainView import MainView

import concurrent.futures

logging.basicConfig(filename='log.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

directory = '.'
expr = sys.argv[1]

#processing_pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)

controller.scan(directory)
controller.grep(expr)

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

urwid.MainLoop(MainView(), palette=[('reversed', 'standout', ''), ('matched', 'dark red', '')], unhandled_input=exit_on_q).run()
