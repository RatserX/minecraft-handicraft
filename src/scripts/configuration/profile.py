from helpers.dictionary_helper import DictionaryHelper
from helpers.print_helper import PrintHelper
from helpers.prompt_helper import PromptHelper
from services.logger_service import LoggerService
from stores.configuration_store import ConfigurationStore
from stores.option_store import OptionStore

class Profile:
    def __init__(self, logger_service: LoggerService) -> None:
        self.__logger_service: LoggerService = logger_service

        self.configure()
    
    def configure(self):
        self.__autorun: dict = ConfigurationStore.autorun
        self.__profile: dict = ConfigurationStore.profile
    
    def load(self):
        if (self.__autorun != None):
            self.__use_autorun()
        else:
            self.__use_prompt()
    
    def __use_autorun(self) -> None:
        profile_key: str = DictionaryHelper.get(self.__autorun, "profile")
        
        if (DictionaryHelper.has(self.__profile, profile_key)):
            OptionStore.profile_key = profile_key
        else:
            raise KeyError(f"Invalid profile key: {profile_key}")
    
    def __use_prompt(self) -> None:
        options: list[str] = DictionaryHelper.keys(self.__profile)
        
        while True:
            self.__logger_service.info_append("Profiles:")
            [self.__logger_service.info_append(f"[{option}] - {DictionaryHelper.get(self.__profile, option, 'name')}") for option in options]
            
            profile_key: str = PromptHelper.input_option("Select profile (Default '$DEFAULT'): ", options, True, options[0])

            if (DictionaryHelper.has(self.__profile, profile_key)):
                OptionStore.profile_key = profile_key

                break
            else:
                PrintHelper.clear_all()
                self.__logger_service.error_append(f"Invalid profile key: {profile_key}")
