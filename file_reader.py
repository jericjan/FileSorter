import os
import sys
def read_my_binary(file):

    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    path_to_file = os.path.abspath(os.path.join(bundle_dir,file))
    print(path_to_file)
    with open(path_to_file, "rb") as f:
       content = f.read()
    return content   