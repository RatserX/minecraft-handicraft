import os

from scripts.execution.helpers.task_helper import TaskHelper
from services.logger_service import LoggerService
from services.widget_service import WidgetService
from stores.configuration_store import ConfigurationStore
from stores.execution_store import ExecutionStore
from stores.option_store import OptionStore
from stores.path_store import PathStore

class Launcher:
    def __init__(self, logger_service: LoggerService, widget_service: WidgetService) -> None:
        self.__logger_service: LoggerService = logger_service
        self.__widget_service: WidgetService = widget_service

        self.configure()
    
    def configure(self):
        self.__launcher: dict = ConfigurationStore.launcher
        
        self.__launcher_key: dict = OptionStore.launcher_key
        self.__platform_name: dict = OptionStore.platform_name
    
    def load(self):
        self.__use_operation()
    
    def __use_operation(self):
        launcher_name: str = self.__launcher[self.__launcher_key]["name"]
        launcher_platform_tasks: list[list[str]] = self.__launcher[self.__launcher_key]["platform"][self.__platform_name]["tasks"]
        launcher_platform_tasks_length: int = len(launcher_platform_tasks)
        
        public_data_directory: str = PathStore.get_public_data_directory()
        ExecutionStore.directory = os.path.join(public_data_directory, "launcher")
        
        self.__logger_service.info_append(f"Launcher Name: {launcher_name}")

        for i in range(launcher_platform_tasks_length):
            arguments: str = launcher_platform_tasks[i]
            command: str = arguments[0]
            
            if (command.__eq__("call")):
                TaskHelper.call(*arguments, logger_service = self.__logger_service)
            elif (command.__eq__("cd")):
                TaskHelper.cd(*arguments)
            elif (command.__eq__("clear")):
                TaskHelper.clear(*arguments, logger_service = self.__logger_service)
            elif (command.__eq__("dialog")):
                TaskHelper.dialog(*arguments, widget_service = self.__widget_service)
            elif (command.__eq__("exit")):
                TaskHelper.exit(*arguments, logger_service = self.__logger_service)
            elif (command.__eq__("java")):
                TaskHelper.java(*arguments, logger_service = self.__logger_service)
            elif (command.__eq__("unzip")):
                TaskHelper.unzip(*arguments, logger_service = self.__logger_service)
            elif (command.__eq__("wget")):
                TaskHelper.wget(*arguments)
