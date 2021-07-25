import os
import string

class PromptHelper:
    def input_numeric(prompt: str, max_number: int = -1, min_number: int = -1, default: int = 0) -> int:
        prompt_template: string.Template = string.Template(prompt)
        prompt = prompt_template.substitute({
            "DEFAULT": default,
            "MAX_NUMBER": max_number,
            "MIN_NUMBER": min_number,
        })
        
        input_numeric: str = input(prompt)
        
        if (not input_numeric):
            return default
        elif (input_numeric.isnumeric()):
            number: int = int(input_numeric)

            if (
                (max_number < 0 or 0 <= max_number >= number (max_number >= 0 and number <= max_number)) and
                (min_number < 0 or (max_number >= 0 and number >= min_number))
            ):
                return number
        
        return None
    
    def input_option(prompt: str, options: list[str], case: bool = True, default: str = None) -> str:
        prompt_template: string.Template = string.Template(prompt)
        prompt = prompt_template.substitute({
            "CASE": case,
            "DEFAULT": default,
        })

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
    
    def input_path(prompt: str, default: str = None) -> str:
        prompt_template: string.Template = string.Template(prompt)
        prompt = prompt_template.substitute({
            "DEFAULT": default,
        })
        
        input_path: str = input(prompt)
        path: str = os.path.normpath(input_path)
        
        if (not input_path):
            return default
        elif (os.path.exists(path)):
            return path
        
        return None
