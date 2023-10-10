import os
from mysh.constants import *


def pwd(args):
    ### 打印目录
    try:
        print(f'{os.getcwd()}\033')

    ### 错误反馈
    except Exception as e:
        print(f'\033[31mError in pwd: {e}\nUsage: \033[32mpwd\033[0m')

    return SHELL_STATUS_RUN