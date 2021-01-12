import json
import os
from unittest import mock

import matplotlib
import numpy as np
from matplotlib import animation
from tqdm import tqdm

from .util import exec_no_show

matplotlib.use("agg")

__all__ = [
    "gen_mock_events",
    "load_events",
    "playback_file",
    "playback_events",
]


def gen_mock_events(events, globals):
    mock_events = []
    for event in events:
        mock_event = mock.Mock()
        for k, v in event.items():
            if k == "fig":
                setattr(mock_event, "canvas", globals[v].canvas)
            elif k == "inaxes":
                setattr(mock_event, "inaxes", globals.get(v, None))
            else:
                setattr(mock_event, k, v)
        mock_events.append(mock_event)
    return mock_events


def load_events(events):
    meta = {}
    if isinstance(events, str):
        with open(events) as f:
            loaded = json.load(f)
            meta["figname"] = loaded["figname"]
            events = loaded["events"]
    return meta, events


def playback_file(events, path, output, prog_bar=True, **kwargs):
    """
    Parameters
    ----------
    events : str
        Path to the json file defining the events or a dictionary of an
        already loaded file.
    path : str
        path to the file to be executed.
    output : str
        The path to the output file
    prog_bar : bool, default: True
        Whether to display a progressbar of animation progress.
    **kwargs :
        Passed through to `FuncAnimation`.
    """
    meta, events = load_events(events)
    figname = meta["figname"]
    gbl = exec_no_show(path)
    playback_events(figname, events, gbl, output, prog_bar=prog_bar, **kwargs)


def playback_events(figname, events, globals, output, prog_bar=True, **kwargs):
    """
    plays back events that have been

    Parameters
    ----------

    """
    print("here1")
    print(globals.keys())
    mock_events = gen_mock_events(events, globals)
    print("here2")

    # hard coding axes. need to make a fake axis and then use transforms better
    # probs need to record the x/y in figure coordinates, then convert back to
    # display coords for mocking the events
    # use the last axis in order to get a high zorder
    (fake_mouse,) = (
        globals[figname]
        .axes[-1]
        .plot(
            [0, 5], [0, 1], "k", marker=6, markersize=15, transform=None, clip_on=False
        )
    )

    if prog_bar:
        pbar = tqdm(total=len(events))

    def init():
        pass

    def animate(i):
        event = mock_events[i]
        globals[figname].canvas.callbacks.process(event.name, event)
        if event.name == "motion_notify_event":
            fake_mouse.set_data(event.x, event.y)

        globals[figname].canvas.draw()
        if prog_bar:
            pbar.update(1)
            if i == len(events) - 1:
                print("done playing back, saving animation")

    interval = kwargs.pop("interval", 40)
    ani = animation.FuncAnimation(
        globals[figname],
        animate,
        range(len(events)),
        init_func=init,
        interval=interval,
        **kwargs
    )
    dirname = os.path.dirname(output)
    if not os.path.exists(dirname) and dirname not in ["", "."]:
        os.makedirs(os.path.dirname(output))
    ani.save(output)