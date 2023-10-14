import os
import signal


def kill(args):
    if len(args) != 2:
        print(f'\033[31mInvalid arguments\nUsage: kill <signal> <pid>')
        return

    sig = args[0]
    pid = args[1]
    os.kill(sig, pid)