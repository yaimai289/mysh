import os
import sys
from mysh.constants import *
from mysh.shell import builtin_commands
from mysh.builtin.redirect import get_stream


def which(args, **kws):
    ### 获取流
    out_stream, err_stream, in_stream = get_stream(**kws)

    command = str(args[0])
    ### 创建路径列表
    result = []

    ### 若为自建函数
    if command in builtin_commands:
        result.append(f'/home/yw/mysh/mysh/builtin/{command}')

    # 获取环境变量及系统路径作为查找路径
    sys_path = [f'{sys.prefix}/bin', '/usr/bin', '/bin', '/usr/sbin', '/sbin']
    environ_path = os.environ.get('PATH', '').strip().split(os.pathsep)
    search_path = list(set(sys_path + environ_path))

    # 分割路径并与命令名拼接
    for p in search_path:
        command_path = os.path.join(p, command)
        # 判断是否为可执行文件
        is_execute = os.access(command_path, os.X_OK)
        if is_execute:
            result.append(command_path)

    # 若路径列表不为空
    if result:
        print(''.join(result), file= out_stream)
    # 若路径列表为空
    else:
        print(f"\033[31mCommand: \033[36m{command[0]} \033[31mnot found in PATH or no access to\033[0m", file= err_stream)

    return SHELL_STATUS_RUN