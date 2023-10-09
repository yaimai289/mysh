import os
from mysh.constants import *

def cd(args):
    path = args[0] if len(args) > 0 else "~"   ### 若无参数默认参数为~

    ### 切换到最近工作目录
    if path == "-":
        dest = os.environ.get('OLDPWD', "")
        ### 报错
        if not dest:
            print("\033[31mOLDPWD not set\033[0m")
            return SHELL_STATUS_RUN 
    else :
        ### 将输入转化成绝对路径
        dest = os.path.expanduser(path)

    ### 更新当前工作目录和最近工作目录
    current_dir = os.getcwd()
    os.putenv("OLDPWD", current_dir)
    os.chdir(dest)
    working_dir = os.getcwd()
    os.putenv("PWD", working_dir)

    return SHELL_STATUS_RUN