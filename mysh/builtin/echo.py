from mysh.constants import *


def echo(args, **kw):
    ### 去除单双引号
    for arg in args:
        arg = str(arg).strip('\'\"')

    ### 空格连接
    args_string = ' '.join(args)

    print(args_string)

    return SHELL_STATUS_RUN
