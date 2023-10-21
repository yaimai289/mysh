from mysh.constants import *
from mysh.builtin.redirect import get_stream


def var_ref(cmd_token, variable, **kws):
    # 获取流
    out_stream, err_stream, in_stream = get_stream(**kws)

    # 初始化状态
    new_status = None

    # 遍历命令列表
    for i in range(0, len(cmd_token)):
        string = cmd_token[i]
        ### 若出现引用符号，存在变量则替换，不存在则报错
        if string.startswith('$'):
            if string[1:] in variable:
                cmd_token[i] = variable[string[1:]]
            else:
                print(f'\033[31mNot found quotable variable: \033[33m{string[1:]}\033[0m', file= err_stream)
                new_status = SHELL_STATUS_RUN

    ### 判断是否需要跳过后续程序
    if new_status == SHELL_STATUS_RUN:
        return cmd_token, SHELL_STATUS_RUN
    else:
        return cmd_token, None


