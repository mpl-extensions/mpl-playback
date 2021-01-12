import collections
import json
from functools import partial
from os import path

from .util import exec_no_show
from ._version import schema_version

__all__ = [
    "possible_events",
    "record_events",
]
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

event_list = []


def print_event(event, fig, inv_locals):
    info2save = [
        e for e in dir(event) if "_" not in e and e not in ["guiEvent", "lastevent"]
    ]
    saved_info = {k: getattr(event, k) for k in info2save}
    saved_info.pop("canvas")
    saved_info["fig"] = inv_locals[fig]
    saved_info["inaxes"] = inv_locals.get(saved_info["inaxes"], None)
    event_list.append(saved_info)


def record_events(fig, events, inv_locals):
    if isinstance(events, str):
        events = [events]
    for e in events:
        fig.canvas.mpl_connect(e, partial(print_event, fig=fig, inv_locals=inv_locals))


if __name__ == "__main__":
    # execute most of the file
    gbls = exec_no_show("file.py")

    # set up recording
    figname = "fig"
    inv_locals = {
        v: k for k, v in gbls.items() if isinstance(v, collections.abc.Hashable)
    }
    record_events(
        gbls[figname],
        ["motion_notify_event", "button_press_event", "button_release_event"],
        inv_locals,
    )

    gbls["plt"].show()

    with open("data.json", "w") as fp:
        json.dump(
            {
                "figname": figname,
                "schema-version": schema_version,
                "events": event_list,
            },
            fp,
        )
