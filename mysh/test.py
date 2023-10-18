a=input()
print(a)


def get_input():
    input_text = readline.get_line_buffer()
    for char in input_text:
        sys.stdout.write(char)
        sys.stdout.flush()