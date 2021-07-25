from helpers.dictionary_helper import DictionaryHelper
from helpers.print_helper import PrintHelper
from helpers.prompt_helper import PromptHelper
from services.logger_service import LoggerService
from stores.configuration_store import ConfigurationStore
from stores.option_store import OptionStore

class Launcher:
    def __init__(self, logger_service: LoggerService) -> None:
        self.__logger_service: LoggerService = logger_service

        self.configure()
    
    def configure(self):
        self.__autorun: dict = ConfigurationStore.autorun
        self.__launcher: dict = ConfigurationStore.launcher
    
    def load(self):
        if (self.__autorun != None):
            self.__use_autorun()
        else:
            self.__use_prompt()
    
    def __use_autorun(self) -> None:
        launcher_key = DictionaryHelper.get(self.__autorun, "launcher")
        
        if (DictionaryHelper.has(self.__launcher, launcher_key)):
            OptionStore.launcher_key = launcher_key
        else:
            raise KeyError(f"Invalid launcher key: {launcher_key}")
    
    def __use_prompt(self) -> None:
        options: list[str] = DictionaryHelper.keys(self.__launcher)
        
        while True:
            self.__logger_service.info_append("Launchers:")
            [self.__logger_service.info_append(f"[{option}] - {DictionaryHelper.get(self.__launcher, option, 'name')}") for option in options]
            
            launcher_key: str = PromptHelper.input_option("Select launcher (Default '$DEFAULT'): ", options, True, options[0])

            if (DictionaryHelper.has(self.__launcher, launcher_key)):
                OptionStore.launcher_key = launcher_key
                
                break
            else:
                PrintHelper.clear_all()
                self.__logger_service.error_append(f"Invalid launcher key: {launcher_key}")
