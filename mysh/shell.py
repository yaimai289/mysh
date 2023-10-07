import os
import sys
import shlex

sys.path.append('/home/yw/mysh')

from mysh.constants import *
from mysh.builtin import *


### 创建内建函数字典
builtin_cmds = {}

### 分割参数
def tokenize(string):
    return shlex.split(string)

def execute(cmd_token):

    ### 拆分命令名与参数
    cmd_name = cmd_token[0]
    cmd_args = cmd_token[1:]

    ### 若为内置函数则直接执行
    if cmd_name in builtin_cmds:
        return builtin_cmds[cmd_name](cmd_args)

    ### 若为外部命令
    else :
        pid = os.fork()  ### 创建子进程

        ### 当前进程为子进程
        if pid == 0:
            os.execvp(cmd_token[0], cmd_token)  ### 替换进程

        ### 当前进程为父进程
        elif pid > 0:
            while True:
                _, status = os.waitpid([pid, 0])  ### 等待子进程
                if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                    break  ### 子进程正常或异常终止，退出等待

        ### 进程错误
        elif pid < 0:
            print("\033[31merror[0m")
    return SHELL_STATUS_RUN


def shell_loop():
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:

        ### 显示命令提示符
        sys.stdout.write("{}{}  ".format(">>> ", os.getcwd() ))
        sys.stdout.flush()

        ### 读取外部命令
        cmd = sys.stdin.readline()

        ### 切分命令
        cmd_token = tokenize(cmd)

        ### 执行命令并获取新状态
        execute(cmd_token)


def register_builtin_cmds(name, func):
    builtin_cmds[name] = func

### 注册内置函数库
def init():
    register_builtin_cmds("cd", cd)
    register_builtin_cmds("exit", exit)


def main():
    init()
    shell_loop()

if __name__ == "__main__":
    main()