import json
from unittest import mock

import numpy as np
from matplotlib import animation
from tqdm import tqdm

import os
from util import exec_no_show

import matplotlib

matplotlib.use("agg")

__all__ = [
    "playback",
]


def playback(events, path, output, prog_bar=True, **kwargs):
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
    if isinstance(events, str):
        with open("data.json") as f:
            loaded = json.load(f)
            figname = loaded["figname"]
            events = loaded["events"]

    gbl = exec_no_show("file.py")
    mock_events = []
    for event in events:
        mock_event = mock.Mock()
        for k, v in event.items():
            if k == "fig":
                setattr(mock_event, "canvas", gbl[v].canvas)
            elif k == "inaxes":
                setattr(mock_event, "inaxes", gbl.get(v, None))
            else:
                setattr(mock_event, k, v)
        mock_events.append(mock_event)

    # hard coding axes. need to make a fake axis and then use transforms better
    # probs need to record the x/y in figure coordinates, then convert back to
    # display coords for mocking the events
    # use the last axis in order to get a high zorder
    (fake_mouse,) = (
        gbl[figname]
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
        gbl[figname].canvas.callbacks.process(event.name, event)
        if event.name == "motion_notify_event":
            fake_mouse.set_data(event.x, event.y)

        gbl[figname].canvas.draw()
        if prog_bar:
            pbar.update(1)
            if i == len(events) - 1:
                print("done playing back, saving animation")

    interval = kwargs.pop("interval", 40)
    ani = animation.FuncAnimation(
        gbl[figname],
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


if __name__ == "__main__":
    playback("data.json", "file.py", "sliders.gif")