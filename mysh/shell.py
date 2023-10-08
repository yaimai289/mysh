import os
import sys
import shlex
import subprocess
import socket
import getpass

### 设置环境变量
sys.path.append('/home/yw/mysh')

### 创建自建函数列表
builtin_cmd = ['cd', 'exit', 'alias', 'which']


from mysh.constants import *   ### 导入常量
from mysh.builtin import *   ### 导入内置函数
from mysh.builtin.alias import aliased_cmd   ### 导入别名字典

### 创建内建函数字典
commands = {}

### 分割参数
def tokenize(string):
    return shlex.split(string)

def execute(cmd_token):

    ### 拆分命令名与参数
    cmd_name = cmd_token[0]
    cmd_args = cmd_token[1:]

    ### 若为内置命令则直接执行
    if cmd_name in commands :
        return commands[cmd_name](cmd_args)

    ### 根据别名执行命令
    if cmd_name in aliased_cmd :
        alias_cmd = tokenize(aliased_cmd[cmd_name])
        alias_cmd_token = alias_cmd + cmd_args
        return execute(alias_cmd_token)

    ### 若为外部命令
    else :
        try:
            result = subprocess.run(cmd_token, capture_output=True, text=True)
            ### 若有标准输出
            if result.stdout:
                print(result.stdout)
            ### 若有标准错误输出
            if result.stderr:
                print(result.stderr)

        ### 错误反馈
        except FileNotFoundError:
            print(f"\033[31mCommand not found: {cmd_name}\033[0m")
        except Exception as e:
            print(f"\033[31mError in executing: {e}[0m")
    return SHELL_STATUS_RUN


def shell_loop():
    while True:

        ### 显示命令提示符
        sys.stdout.write(f'\033[1;31m>\033[1;33m>\033[1;34m> \033[0;32m{getpass.getuser()}@{socket.gethostname()} \033[1;34m{os.getcwd()}  \033[0;0m')
        sys.stdout.flush()

        ### 读取外部命令
        cmd = sys.stdin.readline()

        ### 切分命令
        cmd_token = tokenize(cmd)

        ### 测试
        print('executing command:', cmd_token)
        print('command args:',cmd_token[1:])

        ### 执行命令并获取新状态
        status = execute(cmd_token)

        ### 检查是否为停止状态
        if status == SHELL_STATUS_STOP:
            break


def register_commands(name, func):
    commands[name] = func



### 注册内置函数库
def init():
    register_commands("cd", cd)
    register_commands("exit", exit)
    register_commands("alias", alias)
    register_commands("which", which)


def main():
    init()
    shell_loop()

if __name__ == "__main__":
    main()