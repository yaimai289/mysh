import os


def pwd(args):
    try:
        print(f'{os.getcwd()}\033')
    except Exception as e:
        print(f'\033[31mError in pwd: {e}\nUsage: \033[32mpwd\033[0m')