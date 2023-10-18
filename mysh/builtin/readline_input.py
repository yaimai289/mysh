import os
import sys
import readline
import getpass
import socket
from mysh.builtin.solve_home_dir import solve_home_dir
from mysh.shell import HISTORY_FILE

readline.read_history_file(HISTORY_FILE)

def tab_complete(user_input, complete_index, builtin_commands, external_commands):
    options = list(builtin_commands.keys()) + external_commands
    matches = [opt for opt in options if opt.startswith(user_input)]
    if complete_index < len(matches):
        return matches[complete_index]
    else:
        return None

readline.set_completer(tab_complete)
readline.parse_and_bind('tab: complete')


def readline_input():
    history_index = readline.get_history_length()

    while True:
        try:
            prompt = f'\033[1;31m>\033[1;33m>\033[1;34m> \033[0;32m{getpass.getuser()}@{socket.gethostname()}' + \
            f'\033[0;0m:\033[1;34m{solve_home_dir(os.getcwd())} \033[0;0m'
            user_input = ''
            while True:
                user_input = input(prompt)
                print(f'u: {user_input}')

                if user_input.endswith(''):
                    print('1')
                # 检查是否为空输入
                    if user_input == '':
                        print('2')
                        continue
                    else:
                        print('3')
                        break
                elif user_input == "\x1b[A": # 上方向键
                    history_index -= 1 if history_index > 0 else history_index
                    user_input = readline.get_history_item(history_index)
                elif user_input == "\x1b[B": # 下方向键
                    history_index += 1 if history_index < readline.get_history_length() else history_index
                    user_input = readline.get_history_item(history_index)
                elif user_input == "\x1b[C" or user_input == "\x1b[D": # 左右方向键
                    continue

            readline.add_history(user_input)
            readline.write_history_file(HISTORY_FILE)
            break

        except IndexError or EOFError:
            continue

    return user_input