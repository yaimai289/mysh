import sys
from mysh.constants import *
from mysh.builtin.redirect import get_stream


def echo(args, **kws):
    # 获取流
    out_stream, err_stream, in_stream = get_stream(**kws)

    ### 连接字符串
    for arg in args:
        arg = str(arg).strip('\'\"')

    # 空格连接
    args_string = ' '.join(args)

    # 打印
    print(args_string, file= out_stream)

    return SHELL_STATUS_RUN