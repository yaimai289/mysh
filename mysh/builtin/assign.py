from mysh.constants import *


def assign(cmd_token, *, variable, builtin_commands, external_commands):


    ### 变量赋值
    if len(cmd_token) == 1:
        string = cmd_token[0]
        args = string.split('=')
        if len(args) == 2:
            variable[args[0]] = args[1]
        return variable
    else:
        return SHELL_STATUS_RUN