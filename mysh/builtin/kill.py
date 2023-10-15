import os
import sys
import signal
import subprocess

### 创建信号字典
signals = {}

def sig_register(signal_num, sig):
    signals[signal_num] = sig
    return signals

sig_register(1, signal.SIGHUP)
sig_register(2, signal.SIGINT)
sig_register(3, signal.SIGQUIT)
sig_register(9, signal.SIGKILL)
sig_register(15, signal.SIGTERM)


def kill(args, *, pids, **kw):
    ### 参数不合规范
    if len(args) > 2:
        print(f'\033[31mInvalid arguments\nUsage: kill <option> <pid>\033[0m')


    ### 无参数默认终止主程序
    elif len(args) == 0:
        print(f'\033[31mYou are killing main process, press (Y/n) to confirm: \033[0m', end='')
        char = input()

        ### 确认
        if char == 'Y' or 'y':
            try:
                os.kill(os.getpid(), 15)
            except PermissionError:
                print(f'\033[31mNo permission to kill main process\033[0m')

        else:
            return


    ### 单参数
    elif len(args) == 1:
        arg = args[0]
        if str(arg).startswith('-') and arg[1:] in signals.keys():
            os.kill(os.getpid(), signals[arg[1:]])
        else:
            if arg in pids.keys():
                try:
                    os.kill(arg, signal.SIGTERM)
                except Exception as e:
                    print(f'\033[33mError in kill process"\033[33m{arg}\033[31m": \033[33m{e}\033[0m')
            else:
                print(f'\033[31mPid: "\033[33m{arg}"\033[31m not found\033[0m')


    ### 标准参数
    elif len(args) == 2:
        option = args[0] if args[0].startswith('-') else None
        pid = args[1] if args[1] in pids else None

        ### 无效参数
        if not option or not pid:
            print(f'\033[31mInvalid arguments\nUse help --kill to check usage\033[0m')
        ### 列出所有信号

        elif option == '-l':
            for s in signals.keys():
                print(f'{s}- {signals[s]}\n')

        ### 执行终止命令
        elif option[1:] in signals.keys():
            try:
                sig = option[1:]
                os.kill(pid, signals[sig])
            except Exception as e:
                print(f'\033[33mError in kill process<\033[33m{pid}\033[31m>: \033[33m{e}\033[0m')