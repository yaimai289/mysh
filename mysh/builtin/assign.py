from mysh.constants import *


def assign(cmd_token, variable, builtin_commands, external_commands):
    if len(cmd_token) == 1:
        string = cmd_token[0]
        print(f'string={string}')
        for character in string:
            if character == '=':
                args = string.split('=')
                print(f'args: {args}')
                if args[0] not in builtin_commands and external_commands\
                   and args[1] not in builtin_commands and external_commands:
                    variable[args[0]] = args[1]
                break
        print(variable)
        return variable
    else:
        return SHELL_STATUS_RUN