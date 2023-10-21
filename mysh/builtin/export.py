import os
from mysh.constants import *
from mysh.builtin.redirect import get_stream


def export(args, **kws):
    # 获取流
    out_stream, err_stream, in_stream = get_stream(**kws)

    ### 参数错误，提供帮助信息
    if len(args) != 1:
        print(f'\033[31mUsage: export <VAR>=<value>\033[0m', file= err_stream)
    ### 解析参数并添加到环境变量中
    else:
        var, value = args[0].split('=')
        os.environ[var] = value

    return SHELL_STATUS_RUN