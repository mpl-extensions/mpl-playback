import numpy as np
from matplotlib.axes import Axes, SubplotBase
from matplotlib.figure import Figure

__all__ = [
    "listify_dict",
    "exec_no_show",
    "extract_by_name",
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


def extract_by_name(name, globals):
    """
    https://stackoverflow.com/a/63331128/835607
    """
    loc = {}
    exec(f"__fig = {name}", globals, loc)
    return loc["__fig"]
