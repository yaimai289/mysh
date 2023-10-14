from mysh.constants import *


def alias(args, *, aliased_cmd, **kw):
    if not args:
        ### 若无参数列出所有别名
        for alias_name, command_name in aliased_cmd.items():
            print(f"{alias_name} = {command_name}")
        return SHELL_STATUS_RUN

    alias_args = ' '.join(args).split('=')
    
    if len(alias_args) == 1:
        ### 若参数为一个列出别名或命令
        alias_name = alias_args[0]
        if alias_name in aliased_cmd:
            print(f"{alias_name} = {aliased_cmd[alias_name]}")
        else :
            print(f"\033[31mNo such alias: \033[32m{alias_name}\033[0m")

    elif len(alias_args) == 2:
    ### 分割别名与函数
        alias_name = alias_args[0].strip().replace("'", "").replace('"', '')
        command_name = alias_args[1].strip().replace("'", "").replace('"', '')

    ### 录入别名
        if alias_name in aliased_cmd:
            print(f'\033[31malias_name: \033[33m{alias_name} exists\033[0m')
        elif command_name in globals() and callable(globals()[command_name]):
            aliased_cmd[alias_name] = command_name

    ### 输入命令不符合格式报错
    else:
        print("\033[31mUsage: alias <alias_name> = <command_name>\033[0m")

    return aliased_cmd