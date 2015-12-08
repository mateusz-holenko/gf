#!/usr/bin/python3
import controller

buffer = []
actions = {}
repeat = 0
keys = []
modes = []

def push_mode(mode):
    modes.insert(0, mode)

def pop_mode():
    del(modes[0])

def register(mode, shortcut, action):
    if type(shortcut) is not list:
        shortcut = [shortcut]
    if mode not in actions:
        actions[mode] = {}
    actions[mode][tuple(shortcut)] = action

def unregister(mode, shortcut):
    if type(shortcut) is not list:
        shortcut = [shortcut]
    del(actions[mode][tuple(shortcut)])

def handle_key(key):
    global repeat
    keys.append(key)

    if key == 'esc':
        reset()
    elif key >= '0' and key <= '9' and len(buffer) == 0:
        if repeat == 0:
            repeat = int(key)
        else:
            repeat = repeat * 10 + int(key)
    else:
        buffer.append(key)
        t = tuple(buffer)
        if t in actions[modes[0]]:
            for x in range(0, repeat if repeat != 0 else 1):
                actions[modes[0]][t]()
                controller.main_loop.draw_screen()
            reset()
        elif not _any_chances():
            reset()

    status_changed_callback()

def reset():
    global repeat
    keys.clear()
    buffer.clear()
    repeat = 0

def status_changed_callback():
    pass

def _any_chances():
    found = False
    for action in actions[modes[0]]:
        interrupted = False
        for item in zip(action, tuple(buffer)):
            if item[0] != item[1]:
                interrupted = True
                break
        if not interrupted:
            found = True
            break
    return found

