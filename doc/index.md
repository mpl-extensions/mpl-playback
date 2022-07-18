.. mpl-playback documentation master file, created by
   sphinx-quickstart on Mon Jan 11 19:21:27 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

# Welcome to mpl-playback's documentation!

A library to record and then playback user interactions with a Matplotlib
figure. Also integrates with [sphinx-gallery](https://sphinx-gallery.github.io/stable/index.html)
by providing a custom scraper so docs using widgets will render showing the interactions.
See this in action in the :doc:`Gallery <gallery/index>`.

Inspired by discussions here: https://github.com/matplotlib/matplotlib/issues/19222

## Installation

```bash
pip install mpl-playback
```

```{note}
If you are using for your sphinx-gallery docs build you should pin the version of `mpl-playback`.
```

### Q: Should you use this?
A: Depends on what you want. For one off gifs of interactions it's almost certainly easier to just record your screen to make a gif. But if you want integration with `sphinx-gallery` then this is currently the only option.



```{toctree}
:maxdepth: 3

gallery/index
commandline
sphinx-gallery
contributing
```

### Indices and Tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
