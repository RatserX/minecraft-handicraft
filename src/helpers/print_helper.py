import os

class PrintHelper:
    def clear_all() -> None:
        if os.name in ("dos", "nt"):
            os.system("cls")
        elif os.name in ("linux", "osx", "posix"):
            os.system("clear")
        else:
            print("\n") * 120
    
    def clear_last() -> None:
        VT100_CURSOR_UP = "\x1b[1A"
        VT100_ERASE_LINE = "\x1b[2K"

        print(f"{VT100_CURSOR_UP}{VT100_ERASE_LINE}{VT100_CURSOR_UP}")
