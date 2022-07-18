[![Documentation Status](https://readthedocs.org/projects/pip/badge/?version=stable)](https://pip.pypa.io/en/stable/?badge=stable)


- Generate and playback recordings of user interactions with matplotlib figures.
- Integrates with sphinx gallery to automatically embed interactions in the docs without
needing to manually generate gifs.

See https://mpl-playback.readthedocs.io/en/latest/gallery/index.html for an example of this in action.

Directly inspired by https://github.com/matplotlib/matplotlib/issues/19222

## Command Line Usage

**recording interactions**
To record a json file for later playback:
```bash
python -m mpl_playback.record example_file.py -figures fig --output example_playback.json
```

This will launch example_file.py and record any interactions with the object named `fig`. Then it will be saved to `example_playback.json`. However, the output argument is optional, if not given then the name will be `example_file-playback.json`

**playback interactions in a gif**
To play back the file you must pass both the original python file and the recording json file. You can optionally pass names for the output gif(s) with the `--output` argument, or allow the names to be chosen automatically. 1 gif will be created for each figure that was recorded.

```bash
python -m mpl_playback.playback example_file.py example_playback.json
```


# Q: Should you use this?
A: Depends on what you want. For one off gifs of interactions it's almost certainly easier to just record your screen to make a gif. But if you want integration with `sphinx-gallery` then this is currently the only option.

### Example of a rendered gif:

![example of rendered gif](played-back.gif)
