#!/usr/bin/python3
import controller

history = []

def reset():
    for elem in history:
        undo()

def undo():
    if len(history) == 0:
        return
    items = history.pop()
    for item in items:
        controller.result_walker.insert(item[0], item[1])

def filter(items):
    removed = []
    for index, value in enumerate(controller.result_walker):
        if value not in items:
            removed.append((index, value))
    for index, to_remove in enumerate(removed):
        del controller.result_walker[to_remove[0] - index]
    history.append(removed)

def delete(items):
    removed = []
    for index, value in enumerate(controller.result_walker):
        for item in items:
            if value == item:
                removed.append((index, value))
    for index, to_remove in enumerate(removed):
        del controller.result_walker[to_remove[0] - index]
    history.append(removed)

