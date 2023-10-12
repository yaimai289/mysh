import os
from mysh.constants import *

def cd(args, **kw):
    path = args[0] if len(args) > 0 else "~"   ### 若无参数默认参数为~

    try:
        ### 切换到最近工作目录
        if path == "-":
            dest = os.environ.get('OLDPWD', "")
            print(f'{os.getcwd}')
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

    ### 错误反馈
    except FileNotFoundError:
        print(f'\033[31mNot found \033[33m{path}\00[0m')
    except Exception as e:
        print(f'\033[31mError in cd: \033[33m{e}\033[0m')

    return SHELL_STATUS_RUN