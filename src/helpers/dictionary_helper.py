import typing

class DictionaryHelper:
    def get(dictionary: dict, *keys: typing.Any) -> typing.Any:
        value: dict = dictionary
        
        try:
            for key in keys:
                value = value[key]
        except KeyError:
            return None
        
        return value
    
    def has(dictionary: dict, *keys: typing.Any) -> bool:
        value: dict = dictionary

        try:
            for key in keys:
                value = value[key]
            
            return True
        except:
            return False
    
    def keys(dictionary: dict):
        keys: typing.KeysView = dictionary.keys()

        return list(keys)
    
    def switch(dictionary: dict, key: typing.Any) -> typing.Any:
        default = dictionary.get("default", None)

        return dictionary.get(key, default)
