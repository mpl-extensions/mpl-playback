"""
file heavily based on/taken from the sphinx-gallery version
https://github.com/sphinx-gallery/sphinx-gallery/blob/ecd399e2e60557875d9312a6f5f8dbe4d0dd7a0e/sphinx_gallery/scrapers.py
"""
import os
import re
import sys
from distutils.version import LooseVersion
from pathlib import Path
from textwrap import indent
from warnings import filterwarnings

from sphinx.errors import ExtensionError
from sphinx_gallery.utils import optipng, scale_image
from sphinx_gallery.scrapers import matplotlib_scraper as _matplotlib_scraper

from .playback import playback_events
from .record import record_events


def _import_matplotlib():
    """Import matplotlib safely."""
    # make sure that the Agg backend is set before importing any
    # matplotlib
    import matplotlib

    matplotlib.use("agg")
    matplotlib_backend = matplotlib.get_backend().lower()

    filterwarnings(
        "ignore",
        category=UserWarning,
        message="Matplotlib is currently using agg, which is a"
        " non-GUI backend, so cannot show the figure.",
    )

    if matplotlib_backend != "agg":
        raise ExtensionError(
            "Sphinx-Gallery relies on the matplotlib 'agg' backend to "
            "render figures and write them to files. You are "
            "currently using the {} backend. Sphinx-Gallery will "
            "terminate the build now, because changing backends is "
            "not well supported by matplotlib. We advise you to move "
            "sphinx_gallery imports before any matplotlib-dependent "
            "import. Moving sphinx_gallery imports at the top of "
            "your conf.py file should fix this issue".format(matplotlib_backend)
        )

    import matplotlib.pyplot as plt

    return matplotlib, plt


from pathlib import Path

from mpl_playback.playback import load_events, playback_events

SINGLE_IMAGE = """
.. image:: /{}
    :alt: {}
    :class: sphx-glr-single-img
"""


def matplotlib_scraper(block, block_vars, gallery_conf, **kwargs):
    """
    A drop in replacement for the sphinx-gallery matplotlib scraper that will
    also check if there are playback files associated with the example. In that case
    it will generate a gif using mpl-playback. Looks a file ``_<file name>-playback.json``.

    Rest of docstring is taken directly from sphinx-gallery:

    Scrape Matplotlib images.

    Based on the matplotlib_scraper included in sphinx-gallery

    Parameters
    ----------
    block : tuple
        A tuple containing the (label, content, line_number) of the block.
    block_vars : dict
        Dict of block variables.
    gallery_conf : dict
        Contains the configuration of Sphinx-Gallery
    **kwargs : dict
        Additional keyword arguments to pass to
        :meth:`~matplotlib.figure.Figure.savefig`, e.g. ``format='svg'``.
        The ``format`` kwarg in particular is used to set the file extension
        of the output file (currently only 'png', 'jpg', and 'svg' are
        supported).

    Returns
    -------
    rst : str
        The ReSTructuredText that will be rendered to HTML containing
        the images. This is often produced by :func:`figure_rst`.
    """
    # check if there is a playback file
    p = Path(block_vars["src_file"])
    events_path = p.parent.joinpath(f"_{p.stem}-playback.json")

    if not events_path.exists():
        return _matplotlib_scraper(block, block_vars, gallery_conf, **kwargs)

    matplotlib, plt = _import_matplotlib()
    image_path = next(block_vars["image_path_iterator"]).replace(".png", ".gif")

    meta, events = load_events(str(events_path))
    playback_events(meta["figname"], events, block_vars["example_globals"], image_path)

    image_path_iterator = block_vars["image_path_iterator"]
    image_rsts = []
    plt.close("all")
    rst = SINGLE_IMAGE.format(image_path, "Animated gif of interaction")
    return rst
