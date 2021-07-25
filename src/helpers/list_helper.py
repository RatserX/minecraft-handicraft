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
    
    def range(array: list, start: int, stop: int = -1) -> typing.Any:
        values: list = []

        def __normalize_index(array: list, index: int):
            array_length: int = len(array)

            if (index > array_length):
                return array_length
            elif (index < 0):
                return (array_length + index + 1)
            else:
                return index + 1
        
        start = __normalize_index(array, start)
        stop = __normalize_index(array, stop)
        
        for index in range(start, stop):
            values.append(array[index])
        
        return values
