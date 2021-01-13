import collections
import json
from functools import partial
from os import path
from pathlib import Path

from .util import exec_no_show, listify_dict, extract_by_name
from ._version import schema_version

__all__ = [
    "possible_events",
    "record_events",
    "record_file",
    "record_figure",
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


from matplotlib import axes


import numpy as np


def _find_obj(names, objs, obj, accessors):
    """
    accessors : dict
        A dict of predefined ways to access objects.

    find the name of the figure or axes.
    TODO: Checks in nested lists and tuples
    TODO: check in dictionaries
    """
    if obj is None:
        return None
    if obj in accessors:
        return accessors[obj]

    for name, maybe in zip(names, objs):
        if obj is maybe:
            return name
        if isinstance(maybe, np.ndarray):
            # gotta special case otherwise potential
            # for ValueErrors when doing obj in numpy-array
            if maybe.dtype == np.object:
                if obj in maybe:
                    return name, int(np.where(maybe == obj)[0][0])
        elif isinstance(maybe, (list, tuple)) and obj in maybe:
            return name, maybe.index(obj)
        # elif isinstance(maybe, dict) and obj in maybe:
        #     return _find_in_dict(maybe, dict)
    raise ValueError(
        f"Something has gone wrong while encoding: {str(obj)}"
        " - please report this issue on https://github.com/ianhi/mpl-playback"
    )


def _record_event(event, fig, names, objs, accessors):
    info2save = [
        e for e in dir(event) if "_" not in e and e not in ["guiEvent", "lastevent"]
    ]
    saved_info = {k: getattr(event, k) for k in info2save}
    saved_info.pop("canvas")
    saved_info["fig"] = _find_obj(names, objs, event.canvas.figure, accessors)
    saved_info["inaxes"] = _find_obj(names, objs, saved_info["inaxes"], accessors)
    event_list.append(saved_info)


def record_file(path, fig="fig", output=None):
    """
    Parameters
    ----------

    path : str
        The path to the file to be run
    fig : str, default: fig
        The variable name of the figure to capture. Can
        also be a string that access objects. e.g.:
        ``controls.fig`` or ``list_of_figures[0][1]``.
    output : str or None, default: None
        Defaults to ``_<file-name>-playback.json``
    """
    globals = exec_no_show(path)

    if isinstance(fig, str):
        fig = [fig]
    if output is None:
        output = "_" + Path(path).stem + "-playback.json"
    record_figures(fig, globals, output)


def record_figure(fig, globals, savename, accessors=None):
    record_figures([fig], globals, savename, accessors=None)


def record_figures(figures, globals, savename, accessors=None):
    """
    Parameters
    ----------
    fig : list of str
        list of exec-able calls to obtain the figure.
    globals : dict
    savename : str
    accessors : dict
        Ways to access objects. Useful for figures or axes
    """
    if accessors is None:
        accessors = {}

    for fig in figures:
        _fig = extract_by_name(fig, globals)
        accessors[_fig] = fig
        record_events(
            _fig,
            ["motion_notify_event", "button_press_event", "button_release_event"],
            globals,
            accessors,
        )
    globals["plt"].show()
    with open(savename, "w") as fp:
        json.dump(
            {
                "figures": figures,
                "schema-version": schema_version,
                "events": event_list,
            },
            fp,
        )


def record_events(fig, events, globals, accessors=None):
    if accessors is None:
        accessors = {}
    names, objs = listify_dict(globals)
    if isinstance(events, str):
        events = [events]
    for e in events:
        fig.canvas.mpl_connect(
            e,
            partial(
                _record_event, fig=fig, names=names, objs=objs, accessors=accessors
            ),
        )
