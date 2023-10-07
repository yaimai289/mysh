import os
from mysh.constants import *

def cd(path):
    if len(path) > 0:
        os.chdir(path[0])
    else :
        os.chdir(os.path.expanduser("~"))
    return SHELL_STATUS_RUN