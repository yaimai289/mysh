import readline


def readline_input():
    line = ""
    index = 0
    history_index = -1
    history_length = readline.get_current_history_length()

    while True:
        try:
            # 逐字符读取输入并显示
            char = input()
            
            # 处理特殊按键
            if ord(char) == 3:  # Ctrl+C
                print("^C")
                return None
            elif ord(char) == 27:  # 方向键或其他特殊按键
                char = input()
                if char == "[A":  # 上方向键
                    if history_index < history_length - 1:
                        history_index += 1
                        line = readline.get_history_item(history_index)
                        index = len(line)
                elif char == "[B":  # 下方向键
                    if history_index > -1:
                        history_index -= 1
                        line = readline.get_history_item(history_index)
                        index = len(line)
                elif char == "[C":  # 右方向键
                    if index < len(line):
                        index += 1
                elif char == "[D":  # 左方向键
                    if index > 0:
                        index -= 1
                else:
                    continue
            elif ord(char) == 9:  # Tab键
                # 这里可以实现自动补全的逻辑
                # ...
                continue
                
            # 处理普通字符
            if char == "\n":
                print()  # 换行
                return line
            elif char == "\b":  # 退格键
                if index > 0:
                    line = line[:index-1] + line[index:]
                    index -= 1
            else:
                line = line[:index] + char + line[index:]
                index += 1
            
            # 在光标位置处插入字符并移动光标
            readline.set_startup_hook(lambda: readline.insert_text(line))
            input()
        
        except (KeyboardInterrupt, EOFError):
            print("^C")
            return None

