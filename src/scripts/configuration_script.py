from services.logger_service import LoggerService

from scripts.configuration.launcher import Launcher
from scripts.configuration.platform import Platform
from scripts.configuration.profile import Profile

class ConfigurationScript:
    def __init__(self, logger_service: LoggerService) -> None:
        self.__launcher = Launcher(logger_service)
        self.__platform = Platform(logger_service)
        self.__profile = Profile(logger_service)

        self.load()
    
    def load(self):
        self.__launcher.load()
        self.__platform.load()
        self.__profile.load()
