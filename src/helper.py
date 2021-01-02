import os
import requests
import tqdm
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
        input_numeric: str = input(prompt)
        
        if (not input_numeric):
            return default
        elif (input_numeric.isnumeric()):
            number: int = int(input_numeric)

            if (
                (max_number < 0 or (max_number >= 0 and number <= max_number)) and
                (min_number < 0 or (max_number >= 0 and number >= min_number))
            ):
                return number
        
        return -1

class String:
    def input_option(prompt: typing.Any, options: list[str], case: bool = True, default: str = None) -> str:
        input_option: str = input(prompt)
        parsed_option: str = input_option
        
        if (not input_option):
            return default
        else:
            if (case):
                parsed_option: str = parsed_option.upper()

            for option in options:
                if (case):
                    option: str = option.upper()
                
                if (parsed_option == option):
                    return input_option
        
        return None
    
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
    
    def download_progress(file: str, url: str) -> None:
        with open(file, "wb") as f:
            url_split: list[str] = url.split("/")

            desc: str = url_split[-1]
            response: requests.Response = requests.get(url, stream = True)
            content_length: str = response.headers.get("content-length", 0)
            total: int = int(content_length)

            with tqdm.tqdm.wrapattr(f, "write", desc = desc, miniters = 1, total = total) as fout:
                for buffer in response.iter_content(4096):
                    fout.write(buffer)
