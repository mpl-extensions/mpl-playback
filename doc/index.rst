.. mpl-playback documentation master file, created by
   sphinx-quickstart on Mon Jan 11 19:21:27 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mpl-playback's documentation!
========================================

A library to record and then playback user interactions with a Matplotlib
figure. Also integrates with `sphinx-gallery <https://sphinx-gallery.github.io/stable/index.html>`_
by providing a custom scraper so docs using widgets will render showing the interactions.
See this in action in the :doc:`Gallery <gallery/index>`.

Inspired by discussions here: https://github.com/matplotlib/matplotlib/issues/19222

Q: Should you use this?

A: Probably not. I mainly made this so that I could more easily test widget interactions https://github.com/ianhi/mpl-interactions

For one off gifs of interactions it's almost certainly easier to just record your screen to make a gif.

Developed on https://github.com/ianhi/mpl-playback PRs or comments welcome :)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   gallery/index.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
