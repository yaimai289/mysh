import os
from mysh.shell import HISTORY_FILE


if not os.path.exists(HISTORY_FILE) or not os.path.isfile(HISTORY_FILE):
    with open(HISTORY_FILE, "r"):
        pass


def history(args):
    ### 获取历史命令列表
    with open(HISTORY_FILE, "r") as f:
        lines = f.readlines
    history_num = len(lines)
    load_num = args[0] if len(args) > 0 else history_num   ### 加载命令历史默认为全部

    ### 加载命令历史过多报错
    if load_num > history:
        print(f"\033[31mNot enough command history\nAmount of command history :{len(lines)}")

    ### 若无异常打印命令
    else:
        first_command = history_num - load_num
        for l in lines[first_command:]:
            print(f"{l}\n")


def save_history(cmd_token):
    ### 获取历史命令列表
    with open(HISTORY_FILE, "w") as f:
        lines = f.readlines

    ### 若历史命令数未超过最大值100
    if len(lines) < 100:
        first_command = 0
    ### 若历史命令数超过最大值
    else:
        first_command = 1
    new_lines = lines[first_command:] + [cmd_token]

    ### 写入新历史记录
    with open(HISTORY_FILE, "w") as f:
        f.writelines(new_lines)