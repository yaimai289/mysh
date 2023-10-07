from mysh.constants import *


### 创建别名函数字典
aliased_cmd = {}

def alias(args):
    if not args:
        ### 若无参数列出所有别名
        for alias_name, command in aliased_cmd.items():
            print(f"{alias_name} = {command}")
        return SHELL_STATUS_RUN

    alias_args = args[0].split("=")

    if len(alias_args) == 1:
        ### 若参数为一个列出别名或命令
        alias_name = args[0]
        if alias_name in aliased_cmd:
            print(f"{alias_name} = {aliased_cmd[alias_name]}")
        else :
            print(f"\033[31mNo such alias: {alias_name}\033[0m")

    elif len(alias_args) == 2:
    ### 分割别名与函数
        alias_name = alias_args[0].strip()
        command = alias_args[1].strip().replace("'", "").replace('"', '')

    ### 录入别名
        aliased_cmd[alias_name] = command


    ### 输入命令不符合格式报错
    else:
        print("\033[31mUsage: alias <alias_name> <command>\033[0m")
        return SHELL_STATUS_RUN

    return SHELL_STATUS_RUN