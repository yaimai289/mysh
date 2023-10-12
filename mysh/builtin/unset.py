from mysh.constants import *
from mysh.builtin.alias import aliased_cmd


def unset(args, *, variable, **kw):

    ### 判断格式是否正确
    if len(args) == 1 or 2:
        option = args[0] if len(args) == 2 else '-v'
        arg = args[1] if len(args) else args[0]

        ### 删除别名
        if option == '-a':
            if arg in aliased_cmd:
                del aliased_cmd[arg]
            else:
                print(f'\033[31mNot found alias: \033[33m{arg}\033[0m')

            ### 删除函数
        elif option == '-f':
            if arg in globals():
                fun = globals()[args]
                if callable(fun):
                    del globals()[arg]
            if arg in locals():
                fun = locals()[args]
                if callable(fun):
                    del locals()[arg]
            else:
                print(f'\033[31mNot found function: \033[33m{args}\033[0m')

            ### 删除变量
        elif option == '-v':
            if args in variable:
                del variable[args]
            else:
                print(f'\033[31mNot found variable: {args}')

        else:
            print(f'\033[31mUsage: unset (option) <alias>')

            return SHELL_STATUS_RUN

