from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.axes import SubplotBase
import numpy as np

__all__ = [
    "listify_dict",
    "exec_no_show",
]


def exec_no_show(filepath, globals=None, locals=None):
    """
    exec a file except for plt.show
    """
    if globals is None:
        globals = {}
    globals.update(
        {
            "__file__": filepath,
            "__name__": "__main__",
        }
    )
    with open(filepath) as file:
        block = file.read()
        block = block.replace("plt.show", "")
        exec(compile(block, filepath, "exec"), globals)
    return globals


def listify_dict(d):
    """
    convert a dictionary to a list of names and values filtering only for objects
    that we care about
    """
    names = []
    objs = []
    for k, v in d.items():
        if isinstance(v, (list, tuple, dict, np.ndarray, Axes, SubplotBase, Figure)):
            if isinstance(v, np.ndarray) and not v.dtype == np.object:
                continue
            if "__" in k:
                continue
            names.append(k)
            objs.append(v)
    return names, objs
