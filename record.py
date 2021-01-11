import json

from unittest import mock

from os import path
from functools import partial
import json


possible_events = [
    "button_press_event",
    "button_release_event",
    "draw_event",
    "key_press_event",
    "key_release_event",
    "motion_notify_event",
    "pick_event",
    "resize_event",
    "scroll_event",
    "figure_enter_event",
    "figure_leave_event",
    "axes_enter_event",
    "axes_leave_event",
]
path = path.realpath("file.py")
fxn_globals = {}
fxn_locals = {}


event_list = []


def print_event(event, fig, inv_locals):
    info2save = [
        e for e in dir(event) if "_" not in e and e not in ["guiEvent", "lastevent"]
    ]
    saved_info = {k: getattr(event, k) for k in info2save}
    # print(inv_locals.keys())
    # print(inv_locals[saved_info['canvas']])
    # saved_info['canvas'] = inv_locals[saved_info['canvas'].figure].canvas
    # inaxes = saved_info['inaxes']

    saved_info.pop("canvas")
    saved_info["fig"] = inv_locals[fig]
    saved_info["inaxes"] = inv_locals.get(saved_info["inaxes"], None)
    event_list.append(saved_info)
    # print(saved_info)
    print(event)


def record_events(fig, events, inv_locals):
    if isinstance(events, str):
        events = [events]
    for e in events:
        fig.canvas.mpl_connect(e, partial(print_event, fig=fig, inv_locals=inv_locals))


def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update(
        {
            "__file__": filepath,
            "__name__": "__main__",
        }
    )
    with open(filepath) as file:
        block = file.read()
        block = block.replace("plt.show", "")
        exec(compile(block, filepath, "exec"), globals)
    return globals


# execute the file
import collections

gbls = execfile("file.py")
inv_locals = {v: k for k, v in gbls.items() if isinstance(v, collections.Hashable)}
record_events(
    gbls["fig"],
    ["motion_notify_event", "button_press_event", "button_release_event"],
    inv_locals,
)
gbls["plt"].show()

with open("data.json", "w") as fp:
    json.dump(event_list, fp)
