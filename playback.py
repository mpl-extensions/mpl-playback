import json
from unittest import mock

import numpy as np
from matplotlib import animation
from tqdm import tqdm

import os
from util import exec_no_show


def playback(events, path, output, prog_bar=True, **kwargs):
    """
    Parameters
    ----------
    events : str or dict
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
            event_data = json.load(f)
    else:
        event_data = events

    gbl = exec_no_show("file.py")
    events = []
    for event in event_data:
        events.append([event["name"], mock.Mock()])
        for k, v in event.items():
            if k == "fig":
                setattr(events[-1][1], "canvas", gbl[v].canvas)
            elif k == "inaxes":
                setattr(events[-1][1], "inaxes", gbl.get(v, None))
            else:
                setattr(events[-1][1], k, v)

    # hard coding axes. need to make a fake axis and then use transforms better
    # probs need to record the x/y in figure coordinates, then convert back to
    # display coords for mocking the events
    (fake_mouse,) = gbl["axfreq"].plot(
        [0, 5], [0, 1], "k", marker="^", markersize=15, transform=None, clip_on=False
    )

    if prog_bar:
        pbar = tqdm(total=len(events))

    def init():
        pass

    def animate(i):
        event = events[i]
        gbl["fig"].canvas.callbacks.process(event[0], event[1])
        if event[0] == "motion_notify_event":
            # print('here?')
            fake_mouse.set_data(event[1].x, event[1].y)

        gbl["ax"].set_title(i)
        gbl["fig"].canvas.draw()
        if prog_bar:
            pbar.update(1)
            if i == len(events)-1:
                print("done playing back, saving animation")

    interval = kwargs.pop("interval", 40)
    ani = animation.FuncAnimation(
        gbl["fig"],
        animate,
        range(len(events)),
        init_func=init,
        interval=interval,
        **kwargs
    )
    dirname = os.path.dirname(output)
    if not os.path.exists(dirname) and dirname not in ['', '.']:
        os.makedirs(os.path.dirname(output))
    ani.save(output)


if __name__ == "__main__":
    playback("data.json", "file.py", "sliders.gif")