import json
import os
from unittest import mock

import matplotlib

matplotlib.use("Agg")

import numpy as np
from matplotlib import animation
from matplotlib.animation import FFMpegWriter, ImageMagickWriter, PillowWriter, AVConvWriter
from .util import exec_no_show, listify_dict, extract_by_name
from ._version import schema_version

_prog_bar = True
try:
    from tqdm import tqdm
except ImportError:
    _prog_bar = False

__all__ = [
    "gen_mock_events",
    "load_events",
    "playback_file",
    "playback_events",
]


def _grab_obj(globals, key):
    if isinstance(key, str):
        return globals.get(key, None)
    elif key is None:
        return None
    else:
        base = globals.get(key[0], None)
        if base is None:
            return base
        # TODO - do this in a clever way that generalizes to n deep nesting
        if len(key) == 2:
            return base[key[1]]
        elif len(key) == 3:
            return base[key[1]][key[2]]
        raise ValueError("Nesting beyond 2 levels not yet supported")


def gen_mock_events(events, globals, accessors):
    times = []
    mock_events = []
    for event in events:
        mock_event = mock.Mock()
        for k, v in event.items():
            if k == "time":
                times.append(v)
            elif k == "fig":
                setattr(mock_event, "canvas", accessors[v].canvas)
                setattr(mock_event, "_figname", v)
            elif k == "inaxes":
                setattr(mock_event, "inaxes", _grab_obj(globals, v))
            else:
                setattr(mock_event, k, v)
        mock_events.append(mock_event)
    return np.array(times), np.array(mock_events)


def load_events(events):
    meta = {}
    if isinstance(events, str):
        with open(events) as f:
            loaded = json.load(f)
            meta["figures"] = loaded["figures"]
            meta["schema-version"] = loaded["schema-version"]
            events = loaded["events"]
    return meta, events


def playback_file(
    events,
    path,
    outputs,
    fps=24,
    from_first_event=True,
    prog_bar=True,
    writer="ffmpeg-pillow",
    **kwargs,
):
    """
    Parameters
    ----------
    events : str
        Path to the json file defining the events or a dictionary of an
        already loaded file.
    path : str
        path to the file to be executed.
    outputs : str, list of str, or None
        The path(s) to the output file(s). If None then the
        events will played back but no outputs will saved.
    fps : int, default: 24
        Frames per second of the output
    from_first_event : bool, default: True
        Whether playback should start from the timing of the first recorded
        event or from when recording was initiated.
    prog_bar : bool, default: True
        Whether to display a progress bar. If tqdm is not
        available then this kwarg has no effect.
    writer : str, default: 'ffmpeg-pillow'
        which writer to use. options 'ffmpeg', 'imagemagick', 'avconv', 'pillow'.
        If the chosen writer is not available pillow will be used as a fallback.
    """
    if isinstance(outputs, str):
        outputs = [outputs]
    meta, events = load_events(events)
    figures = meta["figures"]
    gbl = exec_no_show(path)
    playback_events(
        figures,
        events,
        meta,
        gbl,
        outputs,
        fps,
        from_first_event,
        prog_bar=prog_bar,
        writer=writers ** kwargs,
    )


def playback_events(
    figures,
    events,
    meta,
    globals,
    outputs,
    fps=24,
    from_first_event=True,
    prog_bar=True,
    writer="ffmpeg-pillow",
    **kwargs,
):
    """
    plays back events that have been

    Parameters
    ----------
    ....
    outputs : list of str or None
        The paths to outputs. If None then the events will played back but
        no outputs will saved.
    fps : int, default: 24
        Frames per second of the output
    from_first_event : bool, default: True
        Whether playback should start from the timing of the first recorded
        event or from when recording was initiated.
    prog_bar : bool, default: True
        Whether to display a progress bar. If tqdm is not
        available then this kwarg has no effect.
    """
    accessors = {}
    fake_cursors = {}
    writers = []
    if writer == 'ffmpeg' and FFMpegWriter.isAvailable():
        writer = FFMpegWriter
    elif writer == 'imagemagick' and ImageMagickWriter.isAvailable():
        writer = ImageMagickWriter
    elif writer == 'avconv' and AVConvWriter.isAvailable():
        writer = AVConvWriter
    else:
        writer = PillowWriter


    _figs = {}  # the actual figure objects
    transforms = {}
    for fig, out in zip(figures, outputs):
        _fig = extract_by_name(fig, globals)
        _figs[fig] = _fig
        # pre invert for performance (i have no idea if this owuld get cached.)
        # but if it's inverting a matrix then it's bad news to constantly invert
        transforms[fig] = _fig.transFigure.inverted().frozen()
        accessors[fig] = _fig
        fake_cursors[fig] = _fig.axes[-1].plot(
            [0, 0],
            [0, 0],
            "k",
            marker=6,
            markersize=15,
            transform=_fig.transFigure,  # confusing that this is necessary, see note in animate below
            clip_on=False,
            zorder=99999,
        )[0]
        if outputs is not None:
            writers.append(writer(fps))
            writers[-1].setup(_fig, out, len(events))

    times, mock_events = gen_mock_events(events, globals, accessors)
    if from_first_event:
        times -= times[0]
    N_frames = np.int(times[-1] * fps)
    # map from frames to events
    event_frames = np.round(times * fps)

    if prog_bar and _prog_bar:
        pbar = tqdm(total=N_frames)

    def animate(i):
        idx = event_frames == i
        if np.sum(idx) != 0:
            for event in mock_events[idx]:
                # event = mock_events[i]
                accessors[event._figname].canvas.callbacks.process(event.name, event)
                if event.name == "motion_notify_event":
                    # now set the cursor invisible so multiple don't show up
                    # if there are multiple figures
                    for fc in fake_cursors.values():
                        fc.set_visible(False)

                    # It really seems as though this transform should be uncessary
                    # and with only a single figure it is uncesssary. But for reasons that
                    # are beyond me, when there are multiple figures this transform is crucial
                    # or else the cursor will show up in a weirdly scaled position
                    # this is true even with setting `transform=None` on the origin `plot` call
                    f = _figs[event._figname]
                    xy = transforms[event._figname].transform([event.x, event.y])
                    fake_cursors[event._figname].set_data([xy[0]], [xy[1]])
                    fake_cursors[event._figname].set_visible(True)

                # theres got to be a clever way to avoid doing these gazillion draws
                # maybe monkeypatching the figure's draw event?
                for f in _figs.values():
                    f.canvas.draw()

        if prog_bar and _prog_bar:
            pbar.update(1)
        if outputs is not None:
            for w in writers:
                w.grab_frame()

    for i in range(N_frames):
        animate(i)

    if outputs is not None:
        for w in writers:
            w.finish()
