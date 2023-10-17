import sys
from mysh.constants import *
from mysh.builtin.redirect import *

def echo(args, *, out_stream, in_stream, err_stream, **kw):

    #redirect(out_stream, err_stream, in_stream)

    ### 去除单双引号
    for arg in args:
        arg = str(arg).strip('\'\"')

    ### 空格连接
    args_string = ' '.join(args)

    print(args_string)

    return SHELL_STATUS_RUN
