import os
import sys
import getpass
import socket
import termios
import tty
from mysh.builtin.solve_home_dir import solve_home_dir
from mysh.shell import HISTORY_FILE

def tab_complete(user_input, complete_index, builtin_commands, external_commands):
    options = list(builtin_commands.keys()) + external_commands
    matches = [opt for opt in options if opt.startswith(user_input)]
    if complete_index < len(matches):
        return matches[complete_index]
    else:
        return None

def get_history():
    with open(HISTORY_FILE ,'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip('\n')
    return lines

def solve_char(char, complete_index, history_index, cusor, user_input, lines, builtin_commands, external_commands):
    if char == '\x1b[A':
        if history_index > 0:
            history_index -= 1
            user_input = lines[complete_index]
    elif char == '\x1b[B':
        if history_index < len(lines)-1:
            history_index += 1
            user_input = lines[complete_index]
        else:
            user_input = ''
    elif char == '\x1b[C':
        if cusor > -len(user_input):
            cusor -= 1
    elif char == '\x1b[D':
        if cusor < -1:
            cusor += 1
    elif char == '\t':
        if complete_index >= 0:
            complete_index += 1
            result = tab_complete(user_input, complete_index, builtin_commands, external_commands)
            if result:
                user_input = result
    else:
        if cusor == -1:
            user_input += char
        elif cusor < -1 and cusor >= -len(user_input):
            user_input = user_input[:cusor] + char + user_input[cusor+1:]

    return complete_index, history_index, cusor, user_input


def mysh_input(builtin_commands, external_commands):
    prompt = f'\033[1;31m>\033[1;33m>\033[1;34m> \033[0;32m'\
             f'{getpass.getuser()}@{socket.gethostname()}\033[0;0m:'\
             f'\033[1;34m{solve_home_dir(os.getcwd())} \033[0;0m'
    user_input = ''
    lines = get_history()
    complete_index = 0
    history_index = len(lines) - 1
    cusor = -1
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        while True:
            char = sys.stdin.read(1)
            if char == '':
                break
            else:
                complete_index, history_index, cusor, user_input = \
                    solve_char(char, complete_index, history_index, cusor, user_input, 
                           lines, builtin_commands, external_commands)
            user_input = "{:<30}".format(prompt + user_input) + '\r'
            print(user_input, end='')

    except Exception as e:
        print(f'\033[31mError in input: \033[33m{e}\033[0m')

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    return user_input
