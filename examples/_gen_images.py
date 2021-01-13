"""
garbo
"""
from mpl_playback.record import record_file

# record_file("dynamic.py", "fig")
# record_file("subplots.py", "ctrls.fig")
# record_file("multifig.py", ["fig", "slider_fig"])
record_file("multifig.py", ["slider_fig", "fig"])
# record_file("multifig.py", ["slider_fig"])
