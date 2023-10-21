import os
import sys
import shlex
import subprocess
import time
import signal
import psutil


# 设置环境变量
sys.path.append('/home/yw/mysh')


from mysh.constants import *   # 导入常量
from mysh.builtin import *   # 导入内置函数


### 设置路径并创建历史记录文件
HISTORY_FILE = os.path.expanduser('~/mysh_history')
open(HISTORY_FILE, "a").close()


### 创建字典与函数
builtin_commands = {}
external_commands = []
aliased_cmd = {}
variable = {}
pids ={}
redirects = []

### 设置标准输出流和标准输出错误流
out_stream=sys.__stdout__
err_stream=sys.__stderr__
in_stream =sys.__stdin__


# 分割参数
def tokenize(string):
    return shlex.split(string)


def execute(cmd_token):

    # 测试
    print(f'cmd_token: {cmd_token}')

    ### 设置标准输出流和标准输出错误流
    out_stream= sys.stdout
    err_stream=sys.stderr
    in_stream =sys.stdin

    # 获取所有进程pid
    pids = pids_register()

    # 重定向
    cmd_token, out_stream, err_stream, in_stream = redirect(cmd_token, redirects, out_stream, err_stream, in_stream)

    # 初始化管道
    with open(os.path.expanduser('~/Pipe'), 'w') as f:
        pass

    ### 管道符
    if '|' in cmd_token:
        cmd_token = ' '.join(cmd_token).split('|')
        out_stream = open(os.path.expanduser('~/Pipe'), 'w')
        in_stream = sys.__stdin__
        for c in cmd_token:
            execute(tokenize(c))
            in_stream = open(os.path.expanduser('~/Pipe'), 'r')


    # 判断是否为赋值函数
    _, status = assign(cmd_token, variable, out_stream=out_stream, err_stream=err_stream, in_stream=in_stream)

    ### 判断是否存在变量引用
    if status != SHELL_STATUS_RUN:
        cmd_token, status = var_ref(cmd_token, variable, out_stream=out_stream, err_stream=err_stream, in_stream=in_stream)

    ### 拆分命令名与参数
    cmd_name = cmd_token[0]
    cmd_args = cmd_token[1:]

    if status == SHELL_STATUS_RUN:
        pass

    ### 执行后台命令
    elif cmd_token[-1] == '&':
        if len(cmd_token) != 1:
            cmd = ' '.join(cmd_token)[:-1]
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode != 0:
                print(f'\033[31mError in background process: \033[33m{proc.stderr}\033[0m')
        else:
            return


    ### 根据别名执行命令
    elif cmd_name in aliased_cmd:
        alias_cmd = tokenize(aliased_cmd[cmd_name])
        alias_cmd_token = alias_cmd + cmd_args
        return execute(alias_cmd_token)

    ### 若为内置命令则直接执行
    elif cmd_name in builtin_commands :
        return builtin_commands[cmd_name](cmd_args, variable=variable, builtin_commands=builtin_commands, 
               external_commands=external_commands, aliased_cmd=aliased_cmd, pids=pids, out_stream = out_stream, 
               err_stream =err_stream, in_stream = in_stream)

    ### 若为外部命令
    else :
        try:
            if '|' in cmd_token:
                commands = ''.join(cmd_token).split('|')
                for c in commands:
                    result = subprocess.run(c, capture_output=True, text=True,stdout=open(os.path.expanduser('~/Pipe'), 'w')
                                            ,input=open(os.path.expanduser('~/Pipe'), 'r'))

            else:
                result = subprocess.run(cmd_token, capture_output=True, text=True)

                ### 若有标准输出
                if result.stdout and out_stream == sys.stdout:
                    print(result.stdout)
                elif out_stream != sys.stdout:
                    out_stream.write(result.stdout)

                ### 若有标准错误输出
                if result.stderr and err_stream ==sys.stderr:
                    print(result.stderr)
                elif err_stream != sys.stderr:
                    err_stream.write(result.stderr)

        ### 错误反馈
        except FileNotFoundError:
            print(f"\033[31mCommand not found: {cmd_name}\033[0m")
        except Exception as e:
            print(f"\033[31mError in executing: {e}[0m")

    return SHELL_STATUS_RUN


def shell_loop():
    while True:

        pids_register()

        # 读取输入命令
        input_cmd = readline_input()

        # 切分命令
        cmd_token = tokenize(input_cmd)

        # 执行命令并获取新状态
        status = execute(cmd_token)

        ### 恢复流
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        sys.stdin = sys.__stdin__

        ### 检查是否为停止状态
        if status == SHELL_STATUS_STOP:
            break


def register_builtin_commands(name, func):
    builtin_commands[name] = func


def get_all_commands():
    all_commands = []
    # 设置查找路径
    sys_path = [f'{sys.prefix}/bin', '/usr/bin', '/bin', '/usr/sbin', '/sbin']

    for path in sys_path:
        try:
            ### 遍历路径判断是否为非空名文件
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_file and entry.name != '':
                        all_commands.append(entry.name)
        except FileNotFoundError:
            continue
    return all_commands


def register_external_command(builtin_commands, external_commands):
    all_commands = get_all_commands()
    external_commands.clear()

    ### 若不在自建函数中注册到外部命令列表中
    for command in all_commands:
        if command not in builtin_commands and command not in external_commands:
            external_commands.append(command)
    return external_commands


### 获取所有进程pid
def pids_register():
    processes = psutil.process_iter(['pid', 'name'])
    for p in processes:
        pids[p.info['pid']] = p.info['name']
    return pids


### 注册函数库
def init():
    register_builtin_commands("cd", cd)
    register_builtin_commands("exit", exit)
    register_builtin_commands("alias", alias)
    register_builtin_commands("which", which)
    register_builtin_commands("history", history)
    register_builtin_commands("echo", echo)
    register_builtin_commands("pwd", pwd)
    register_builtin_commands("type", type)
    register_builtin_commands("export", export)
    register_builtin_commands("unset", unset)
    register_builtin_commands("kill", kill)
    register_external_command(builtin_commands, external_commands)


### 注册重定向符号
redirects = ["<", ">", '2>', '>>']

### 信号处理
pids_register()

def sigint(signal, frame):
    print('\033[33m\nProcess interrupted\033[0m')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint)

def sigterm(signal ,frame):
    for p in pids.keys():
        if p != 0:
            os.kill(p, 15)
    sys.exit(0)
signal.signal(signal.SIGTERM, sigterm)


def main():
    init()
    shell_loop()

if __name__ == "__main__":
    main()