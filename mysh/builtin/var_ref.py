
def var_ref(cmd_token, *, variable, **kw):
    ### 遍历命令列表
    for i in range(0, len(cmd_token)):
        string = cmd_token[i]
        ### 若出现引用符号，存在变量则替换，不存在则报错
        if string[0] == '$':
            if string[1:] in variable:
                print(cmd_token)
                cmd_token[i] = variable[string[1:]]
            else:
                print(f'\033[31mNot found quotable variable: \033[33m{string[1:]}\033[0m')
        else:
            pass
    return cmd_token

