import os
import sys
import readline
import getpass
import socket
from mysh.builtin.solve_home_dir import solve_home_dir
from mysh.shell import HISTORY_FILE

readline.read_history_file(HISTORY_FILE)


### 设定常用自动补全命令
commands = ['ls', 'cd', 'pwd', 'mkdir', 'rm', 'cp', 'mv', 'touch', 'cat', 'grep','find', 'chmod', 'chown', 'ssh', 
            'scp', 'git', 'python', 'pip', 'docker','wget', 'curl', 'tar', 'zip', 'unzip', 'sed', 'awk', 'head', 
            'tail', 'sort','uniq', 'date']
directory = os.listdir(os.getcwd())


### 自动补全功能
def tab_complete(text, state):
    matches = [c for c in commands if c.startswith(text)]
    if state < len(matches):
        return matches[state]
    else:
        return None

### 设定自定补全
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

                if user_input.endswith(''):
                # 检查是否为空输入
                    if user_input == '':
                        continue
                    else:
                        break
                # 上方向键
                elif user_input == "\x1b[A": 
                    history_index -= 1 if history_index > 0 else history_index
                    user_input = readline.get_history_item(history_index)
                            
                # 下方向键
                elif user_input == "\x1b[B": 
                    history_index += 1 if history_index < readline.get_history_length() else history_index
                    user_input = readline.get_history_item(history_index)
                            
                # 左右方向键
                elif user_input == "\x1b[C" or user_input == "\x1b[D": 
                    continue
                            
            # 保存命令历史
            readline.write_history_file(HISTORY_FILE)
            break

        except IndexError or EOFError:
            continue

    return user_input
