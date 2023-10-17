import os
import sys
from mysh.shell import tokenize


def redirect(cmd_token, redirects, out_stream, err_stream, in_stream):
    ### 重定向
    n = None

    for redirect_index in range(0, len(cmd_token)):
        if cmd_token[redirect_index] in redirects:
            redi_sym = cmd_token[redirect_index]
            n = redirect_index
            if n == 0 or n == len(cmd_token) - 1:
                print('\033[31mNo redirect object\033[0m')
                n = None
                break
    if n:
        cmd_target = os.path.expanduser(cmd_token[-1])
        cmd_token = cmd_token[0:n]

        if redi_sym == '>' or '>>':
            ### 重定向到标准输出
            if redi_sym == '>':
                out_stream = open(cmd_target, "w")
            elif redi_sym == '>>':
                out_stream = open(cmd_target, "a")

        elif redi_sym == '2>':
            ### 重定向到标准错误输出
            err_stream = open(cmd_target, "w")

        elif redi_sym == '<':
            ### 重定向到标准输入
            in_stream = open(cmd_target, "r")

    return cmd_token, out_stream, err_stream, in_stream



def get_stream(**kws):
    out_stream = kws.get('out_stream')
    err_stream = kws.get('err_stream')
    in_stream = kws.get('in_stream')
    return out_stream, err_stream, in_stream


def pipe(cmd_token, redirects, out_stream, err_stream, in_stream):
    if '|' in cmd_token:
        cmd_token = ''.join(cmd_token).split('|')
        with open(os.path.expanduser('~/Pipe'), 'w') as f:
            f.truncate(0)
        out_stream = open(os.path.expanduser('~/Pipe'), 'w')
        in_stream = sys.__stdin__
        for c in cmd_token:
            c = tokenize(c)
            