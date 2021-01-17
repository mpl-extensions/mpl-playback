[![Documentation Status](https://readthedocs.org/projects/pip/badge/?version=stable)](https://pip.pypa.io/en/stable/?badge=stable)


- Generate and playback recordings of user interactions with matplotlib figures.
- Integrates with sphinx gallery to automatically embed interactions in the docs without
needing to manually generate gifs.

See https://mpl-playback.readthedocs.io/en/latest/gallery/index.html for an example of this in action.

Directly inspired by https://github.com/matplotlib/matplotlib/issues/19222

# Q: Should you use this?
A: Probably not. I mainly made this so that I could more easily test widget interactions https://github.com/ianhi/mpl-interactions

For one off gifs of interactions it's almost certainly easier to just record your screen to make a gif.

### Example of a rendered gif:

![example of rendered gif](played-back.gif)
