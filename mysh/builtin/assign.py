from mysh.constants import *
from mysh.builtin.redirect import get_stream


def assign(cmd_token, variable, **kws):
    # 获取流
    out_stream, err_stream, in_stream = get_stream(**kws)

    # 初始化状态
    new_status = None

    ### 变量赋值
    if len(cmd_token) == 1:
        string = cmd_token[0]
        args = string.split('=')
        if len(args) == 2:
            variable[args[0]] = args[1]
            new_status = SHELL_STATUS_RUN

    ### 判断是否需要跳过后续程序
    if new_status == SHELL_STATUS_RUN:
        return variable, SHELL_STATUS_RUN
    else:
        return variable, None