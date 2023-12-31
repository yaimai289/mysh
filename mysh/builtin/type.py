from mysh.constants import *
from mysh.builtin.redirect import get_stream


def type(args, *, builtin_commands, external_commands, **kws):
    # 获取流
    out_stream, err_stream, in_stream = get_stream(**kws)

    ### 参数不符合格式
    if len(args) != 1:
        print(f'\033[31mInvalid arguments\nUsage: type <command_name>\033[0m', file= err_stream)
        return SHELL_STATUS_RUN

    command_name = args[0]
    ### 判断命令类型
    if command_name in builtin_commands :
        print(f'Type of <{command_name}>: buit-in command', file= out_stream)
    elif command_name in external_commands :
        print(f'Type of <{command_name}>: external command', file= out_stream)
    
    ### 不存在报错
    else:
        print(f'\033[31mNot found command: \033[33m{command_name}\033[0m', file= err_stream)

        return SHELL_STATUS_RUN