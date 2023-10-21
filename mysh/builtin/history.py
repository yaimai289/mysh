from mysh.shell import HISTORY_FILE
from mysh.builtin.redirect import get_stream


def history(args, **kws):
    # 获取流
    out_stream, err_stream, in_stream = get_stream(**kws)

    try:
        ### 获取历史命令列表
        with open(HISTORY_FILE, "r") as f:
            lines = f.readlines()
        history_num = len(lines)
        load_num = int(args)[0] if len(args) > 0 else history_num   # 加载命令历史默认为全部

        ### 若无命令历史记录
        if history_num == 2:
            print(f'\033[31mNo commnd in history\033[0m', file= err_stream)

        ### 加载命令历史过多报错
        elif load_num > history_num:
            print(f"\033[31mNot enough command history\nAmount of command history : \033[32m{len(lines)}\033[0m", file= err_stream)

        ### 若无异常打印命令
        else:
            first_command = history_num - load_num + 1
            last_command = history_num - 1
            i=0
            for l in lines[first_command:last_command]:
                i += 1
                print(f"{i}. {l}", file= out_stream)
    except Exception as e:
        print(f'\033[31mError in history: \033[32m{e}\033[0m', file= err_stream)