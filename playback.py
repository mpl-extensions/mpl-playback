import json
from unittest import mock

import numpy as np
from matplotlib import animation
from tqdm import tqdm

from util import exec_no_show

with open("data.json") as f:
    event_data = json.load(f)


def init():
    pass


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


pbar = tqdm(total=len(events))


def animate(i):
    event = events[i]
    gbl["fig"].canvas.callbacks.process(event[0], event[1])
    if event[0] == "motion_notify_event":
        # print('here?')
        fake_mouse.set_data(event[1].x, event[1].y)

    gbl["ax"].set_title(i)
    gbl["fig"].canvas.draw()
    pbar.update(1)
    # print(i)


ani = animation.FuncAnimation(
    gbl["fig"],
    animate,
    range(len(events)),
    init_func=init,
    interval=40,
    blit=False,
    repeat=False,
)
ani.save("played-back.gif")
# gbl['plt'].show()
