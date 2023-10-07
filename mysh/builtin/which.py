import os
from mysh.constants import *

def which(command):

    ### 创建路径列表
    result = []

    ### 获取环境变量作为查找路径
    path = os.environ.get('PATH', '').split(os.pathsep)

    ### 分割路径并与命令名拼接
    for p in path:
        command_path = os.path.join(p, str(command))
        ### 判断路径类型及访问权限
        if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
            result.append(command_path)

    ### 若路径列表不为空
    if len (result) > 0:
        print('\n'.join(result))
    ### 若路径列表为空
    else:
        print(f"\033[31mCommand: {command} not found in PATH or no access to\033[0m")

    return SHELL_STATUS_RUN