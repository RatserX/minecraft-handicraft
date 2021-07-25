from services.logger_service import LoggerService
from services.widget_service import WidgetService

from scripts.execution.launcher import Launcher
from scripts.execution.profile import Profile

class ExecutionScript:
    def __init__(self, logger_service: LoggerService, widget_service: WidgetService) -> None:
        self.__launcher = Launcher(logger_service, widget_service)
        self.__profile = Profile(logger_service, widget_service)

        self.load()
    
    def load(self):
        self.__launcher.load()
        self.__profile.load()
