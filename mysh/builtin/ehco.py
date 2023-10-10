from mysh.constants import *


def echo(args):

    for arg in args:
        arg = str(arg).strip('\'\"')
    args_string = ' '.join(args)
    print(args_string)

    return SHELL_STATUS_RUN
