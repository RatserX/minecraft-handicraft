from helpers.platform_helper import PlatformHelper
from services.logger_service import LoggerService
from stores.option_store import OptionStore

class Platform:
    def __init__(self, logger_service: LoggerService) -> None:
        self.__logger_service: LoggerService = logger_service
    
    def load(self):
        self.__use_system()
    
    def __use_system(self) -> None:
        if (PlatformHelper.is_linux()):
            OptionStore.platform_name = "linux"
        elif (PlatformHelper.is_osx()):
            OptionStore.platform_name = "osx"
        elif (PlatformHelper.is_windows()):
            OptionStore.platform_name = "windows"
        else:
            OptionStore.platform_name = "none"
        
        self.__logger_service.info_append(f"Platform: {OptionStore.platform_name}")
