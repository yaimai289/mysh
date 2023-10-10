import os


def solve_home_dir(path):
    home_path = os.path.expanduser('~')
    rel_path = os.path.relpath(path, home_path)
    if rel_path.startswith('.'):
        path = '~'
    elif not rel_path.startswith('..'):
        path = '~' + os.path.sep + rel_path
    return path
