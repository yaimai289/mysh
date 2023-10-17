import sys

def redirect(out_stream, err_stream, in_stream):

    sys.stdout = out_stream
    sys.stderr = err_stream
    sys.stdin = in_stream
