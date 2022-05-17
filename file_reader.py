"""
This allows reading my own added files to work for the single .exe version of File Sorter,
while also still usable with the zipped version.
"""

import os
import sys


def read_my_binary(file):
    """
    This will try to get the _MEIPASS attribute of sys.
    If it succeeds, program is in a temp folder and will use that folder.
    Otherwise, it will use the usual path.
    """
    bundle_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
    path_to_file = os.path.abspath(os.path.join(bundle_dir, file))
    print(path_to_file)
    with open(path_to_file, "rb") as f:
        content = f.read()
    return content
