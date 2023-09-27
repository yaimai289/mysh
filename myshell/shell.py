import os
import sys
import shlex
# 导入常量
from myshell.constants import *
from myshell.sh_builtins import *

# 哈希映射存储内建函数名及引用
built_in_cmds = {}

def tokenize(string):
    return shlex.split(string)


def execute(cmd_tokens):
    #拆分命令名与参数
    cmd_name= cmd_tokens[0]
    cmd_args = cmd_tokens[1:]

    # 若为内置命令则直接调用
    if cmd_name in built_in_cmds:
        return built_in_cmds[cmd_name](cmd_args)

    # 创建子进程
    pid = os.fork()
    if pid == 0:     #为子进程
    # 用exec调用的程序替换该进程
        os.execvp(cmd_tokens[0],cmd_tokens)
    elif pid > 0:     # 为父进程
        while True:     # 等待子进程响应状态
            wpid, status = os.waitpid(pid, 0)

            #子进程正常退出或信号中断时，结束等待状态
            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                break

    # 返回状态
    return SHELL_STATUS_RUN

def shell_loop():
    status = SHELL_STATUS_RUN

    while status ==SHELL_STATUS_RUN:
        # 显示命令提示符
        sys.stdout.write('>>>')
        sys.stdout.flush

        # 读取命令输入
        cmd =sys.stdin.readline()

        # 切分命令输入
        cmd_tokens = tokenize(cmd)

        # 执行命令并获取新的状态
        status = execute(cmd_tokens)

# 注册内建函数到内建命令的哈希映射中
def register_command(name, func):
    built_in_cmds[name] = func

# 注册所有内建命令
def init():
    register_command("cd", cd)
 
def main():
    init()     # 初始化shell
    shell_loop()


if __name__ == "__main__":
    main()