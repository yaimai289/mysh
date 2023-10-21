import os


def solve_home_dir(path):
    ### 计算相对路径
    home_path = os.path.expanduser('~')
    rel_path = os.path.relpath(path, home_path)

    # 若为家目录
    if rel_path.startswith('.'):
        path = '~'

    # 若不在在目录中
    elif not rel_path.startswith('..'):
        path = '~' + os.path.sep + rel_path

    return path
