import sys
from mysh.constants import *
from mysh.builtin.redirect import *

def echo(args, *, out_stream, in_stream, err_stream, **kw):


    for arg in args:
        arg = str(arg).strip('\'\"')

    ### 空格连接
    args_string = ' '.join(args)

    ### 非重定向
    print(args_string)

    return SHELL_STATUS_RUN
