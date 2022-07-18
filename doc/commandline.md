# Command Line Usage

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
