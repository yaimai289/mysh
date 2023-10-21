import os
from mysh.constants import *
from mysh.builtin.redirect import get_stream


def pwd(args, **kws):
    # 获取流
    out_stream, err_stream, in_stream = get_stream(**kws)

    # 打印目录
    try:
        print(f'{os.getcwd()}\033', file= out_stream)

    # 错误反馈
    except Exception as e:
        print(f'\033[31mError in pwd: {e}\nUsage: \033[32mpwd\033[0m')

    return SHELL_STATUS_RUN