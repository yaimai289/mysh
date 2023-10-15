import os
import signal

signals = {}

def sig_register(signals, signal_num, sig):
    signals[signal_num] = sig
    return signals

sig_register(1, signal.SIGHUP)
sig_register(2, signal.SIGINT)
sig_register(3, signal.SIGQUIT)
sig_register(9, signal.SIGKILL)
sig_register(15, signal.SIGTERM)

def kill(args, *, pids):
    if len(args) > 2:
        print(f'\033[31mInvalid arguments\nUsage: kill <option> <pid>\033[0m')
    elif len(args) == 0:
        os.kill(os.getpid, signal.SIGTERM)
    elif len(args) == 1:
        arg = args[0]
        if str(arg).startswith('-') and arg[1:] in signals.keys():
            os.kill(os.getpid(), signals[arg[1:]])
        else:
            if arg in pids.keys():
                try:
                    os.kill(arg, signal.SIGTERM)
                except Exception as e:
                    print(f'\033[33mError in kill process<\033[33m{arg}\033[31m>: \033[33m{e}\033[0m')
            else:
                print(f'\033[31mPid or proccess name: \033[33m{arg} not found\033[0m')
    elif len(args) == 2:
        option = args[0] if args[0].startswith('-') else None
        pid = args[1] if args[1] in pids else None
        if not option or not pid:
            print(f'\033[31mInvalid arguments\nUse help --kill to check usage\033[0m')
        elif option == '-l':
            for s in signals.keys():
                print(f'{s}- {signals[s]}\n')
        elif option in signals.keys() and option[1:] in signals.keys():
            try:
                sig = option[1:]
                os.kill(pid, signals[sig])
            except Exception as e:
                print(f'\033[33mError in kill process<\033[33m{pid}\033[31m>: \033[33m{e}\033[0m')