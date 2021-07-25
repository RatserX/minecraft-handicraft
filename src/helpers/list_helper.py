import typing

class ListHelper:
    def get(array: list, *indexes: int) -> typing.Any:
        value: list = array
        
        try:
            for index in indexes:
                value = value[index]
        except IndexError:
            return None
        
        return value
    
    def has(array: list, *indexes: int) -> bool:
        value: dict = array

        try:
            for index in indexes:
                value = value[index]
            
            return True
        except:
            return False
