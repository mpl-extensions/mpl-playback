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
