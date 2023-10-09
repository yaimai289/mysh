from mysh.shell import HISTORY_FILE

def history(args):
    try:
        ### 获取历史命令列表
        with open(HISTORY_FILE, "r") as f:
            lines = f.readlines()
        history_num = len(lines)
        load_num = int(args)[0] if len(args) > 0 else history_num   ### 加载命令历史默认为全部

        ### 若无命令历史记录
        if history_num == 2:
            print(f'\033[31mNo commnd in history\033[0m')

        ### 加载命令历史过多报错
        elif load_num > history_num:
            print(f"\033[31mNot enough command history\nAmount of command history : \033[32m{len(lines)}\033[0m")

         ### 若无异常打印命令
        else:
            first_command = history_num - load_num + 1
            last_command = history_num - 1
            i=0
            for l in lines[first_command:last_command]:
                i += 1
                print(f"{i}. {l}")
    except Exception as e:
        print(f'\033[31mError in history: \033[32m{e}\033[0m')


def save_history(cmd_token):
    cmd_str = ''.join(cmd_token)

    ### 获取历史命令列表
    with open(HISTORY_FILE, "r") as f:
        lines = f.readlines()

    ### 若历史命令数未超过最大值100
    if len(lines) < 100:
        first_command = 0
    ### 若历史命令数超过最大值
    else:
        first_command = 1
    new_lines = lines[first_command:] + [cmd_str+'\n'] if len(lines) != 0 else [cmd_str]

    ### 写入新历史记录
    with open(HISTORY_FILE, "w") as f:
        f.write("".join(new_lines))