import os
import typing

class Boolean:
    def has_nested_key(dictionary: dict, *keys: typing.Tuple) -> bool:
        value = dictionary

        for key in keys:
            try:
                value = value[key]
            except KeyError:
                return False
        
        return True

class Number:
    def input_numeric(prompt: typing.Any, max_number: int = -1, min_number: int = -1, default: int = 0) -> int:
        input_x: str = input(prompt)
        
        if (not input_x):
            return default
        elif (input_x.isnumeric()):
            number: int = int(input_x)

            if (
                (max_number < 0 or (max_number >= 0 and number <= max_number)) and
                (min_number < 0 or (max_number >= 0 and number >= min_number))
            ):
                return number
        
        return -1

class String:
    def input_path(prompt: typing.Any, default: str = None) -> str:
        input_path: str = input(prompt)
        path: str = os.path.normpath(input_path)
        
        if (not input_path):
            return default
        elif (os.path.exists(path)):
            return path
        
        return None

class Void:
    def deprint() -> None:
        VT100_CURSOR_UP = "\x1b[1A"
        VT100_ERASE_LINE = "\x1b[2K"

        print(f"{VT100_CURSOR_UP}{VT100_ERASE_LINE}{VT100_CURSOR_UP}")
