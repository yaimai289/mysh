import os
import signal
import time
from mysh.builtin.redirect import get_stream


### 获取信号字典
signals = {name.value: name.name for name in signal.Signals}


def kill(args, *, pids, **kws):
    ### 获取流
    out_stream, err_stream, in_stream = get_stream(**kws)

    ### 参数不合规范
    if len(args) > 2:
        print(f'\033[31mInvalid arguments\nUsage: kill <option> <pid>\033[0m', file= err_stream)


    ### 无参数默认终止主程序
    elif len(args) == 0:
        time.sleep(0.5)
        char = input(f'\033[31mYou are killing main process, press (Y/n) to confirm: \033[0m', file= err_stream)
        ### 确认
        if char == 'Y' or 'y':
            try:
                time.sleep(0.5)
                os.kill(os.getpid(), 15)
            except PermissionError:
                print(f'\033[31mNo permission to kill main process\033[0m', file= err_stream)

        else:
            return


    ### 单参数
    elif len(args) == 1:
        ### 默认进程为当前进程
        arg = args[0]
        if str(arg).startswith('-') and arg[1:] in signals.keys():
            os.kill(os.getpid(), signals[arg[1:]])

        ### 列出所有信号
        elif args[0].startswith('-') and args[0] == '-l':
            for s in signals.keys():
                print(f'{s} - {signals[s]}', file= out_stream)

        ### 默认信号为终止信号
        else:
            if arg in pids.keys():
                try:
                    os.kill(arg, signal.SIGTERM)
                except Exception as e:
                    print(f'\033[33mError in kill process"\033[33m{arg}\033[31m": \033[33m{e}\033[0m', file= err_stream)
            else:
                print(f'\033[31mPid: "\033[33m{arg}"\033[31m not found\033[0m', file= err_stream)


    ### 标准参数
    elif len(args) == 2:
        option = args[0] if args[0].startswith('-') else None
        pid = args[1] if args[1] in pids else None

        ### 无效参数
        if not option or not pid:
            print(f'\033[31mInvalid arguments\nUse help --kill to check usage\033[0m', file= err_stream)

        ### 执行终止命令
        elif option[1:] in signals.keys():
            try:
                sig = option[1:]
                time.sleep(0.5)
                os.kill(pid, signals[sig])
            except Exception as e:
                print(f'\033[33mError in kill process<\033[33m{pid}\033[31m>: \033[33m{e}\033[0m', file= err_stream)