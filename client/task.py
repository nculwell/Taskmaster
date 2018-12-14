#!/usr/bin/python3

import os, json

def _checkKeys(dictionary, keys):
    for k in keys:
        x = dictionary[k]

class Task:

    def __init__(self, props):
        _checkKeys(props, ("id", "type", "title"))
        self._props = props

    id = property(lambda self: self._props["id"])
    type = property(lambda self: self._props["type"])
    title = property(lambda self: self._props["title"])

    def ToDict(self):
        return dict(self._props)

def LoadTaskList(filename):
    with open(filename, "r") as f:
        tasks = json.load(f)
    if not isinstance(tasks, (list,)):
        raise Exception("Object loaded as task list is not a list.")
    return [ Task(t) for t in tasks ]

def SaveTaskList(filename, tasks):
    data = ( t.ToDict() for t in tasks )
    try:
        tempfile = filename + ".tmp"
        with open(tempfile, "w") as f:
            json.dump(data, f)
        os.remove(filename)
        os.rename(tempfile, filename)
    finally:
        # Make sure tempfile is gone.
        try:
            os.remove(tempfile)
        except:
            pass

