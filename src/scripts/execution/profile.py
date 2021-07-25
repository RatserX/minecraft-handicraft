import os
import typing
import string
import validators

from helpers.dictionary_helper import DictionaryHelper
from helpers.http_helper import HttpHelper
from helpers.io_helper import IoHelper
from scripts.execution.helpers.task_helper import TaskHelper
from services.logger_service import LoggerService
from services.widget_service import WidgetService
from stores.configuration_store import ConfigurationStore
from stores.execution_store import ExecutionStore
from stores.option_store import OptionStore
from stores.path_store import PathStore

class Profile:
    def __init__(self, logger_service: LoggerService, widget_service: WidgetService) -> None:
        self.__logger_service: LoggerService = logger_service
        self.__widget_service: WidgetService = widget_service

        self.configure()
    
    def configure(self):
        self.__launcher: dict = ConfigurationStore.launcher
        self.__profile: dict = ConfigurationStore.profile
        
        self.__launcher_key: dict = OptionStore.launcher_key
        self.__platform_name: dict = OptionStore.platform_name
        self.__profile_key: dict = OptionStore.profile_key
    
    def load(self):
        self.__use_operation()
    
    def __use_operation(self):
        launcher_platform_data: str = DictionaryHelper.get(self.__launcher, self.__launcher_key, "platform", self.__platform_name, "data")
        profile_location: str = self.__profile[self.__profile_key]["location"]
        profile_name: str = self.__profile[self.__profile_key]["name"]
        profile_tasks: list[list[str]] = self.__profile[self.__profile_key]["tasks"]
        profile_tasks_length: int = len(profile_tasks)
        
        self.__logger_service.info_append(f"Profile Name: {profile_name}")

        substitute_mapping: typing.Mapping[str, object] = {
            "HOME_DIRECTORY": PathStore.home_directory,
            "PROFILE_NAME": profile_name,
            "PUBLIC_DATA_DIRECTORY": PathStore.get_public_data_directory(),
            "PUBLIC_PROFILE_DIRECTORY": PathStore.get_public_profile_directory()
        }
        
        profile_location_template: string.Template = string.Template(profile_location)
        profile_location_file: str = profile_location_template.substitute(substitute_mapping)
        
        instance: dict = {}

        if (validators.url(profile_location_file)):
            instance = HttpHelper.get_json(profile_location_file)
        else:
            instance = IoHelper.get_json(profile_location_file)
        
        basemodloader_downloadurl: str = instance["baseModLoader"]["downloadUrl"]
        basemodloader_filename: str = instance["baseModLoader"]["filename"]
        basemodloader_forgeversion: str = instance["baseModLoader"]["forgeVersion"]
        basemodloader_minecraftversion: str = instance["baseModLoader"]["minecraftVersion"]
        basemodloader_name: str = instance["baseModLoader"]["name"]
        
        self.__logger_service.info_append(f"Base Mod Loader - Forge Version: {basemodloader_forgeversion}")
        self.__logger_service.info_append(f"Base Mod Loader - Minecraft Version: {basemodloader_minecraftversion}")
        self.__logger_service.info_append(f"Base Mod Loader - Name: {basemodloader_name}")
        
        launcher_platform_data = (os.path.normpath(launcher_platform_data) if (launcher_platform_data != None) else "$PUBLIC_DATA_DIRECTORY/profile")
        launcher_platform_data_template: string.Template = string.Template(launcher_platform_data)
        launcher_platform_data_directory: str = launcher_platform_data_template.substitute(substitute_mapping)
        
        data_basemodloader_file: str = os.path.join(launcher_platform_data_directory, basemodloader_filename)
        data_mods_directory: str = os.path.join(launcher_platform_data_directory, "mods")
        
        ExecutionStore.directory = launcher_platform_data_directory

        for i in range(profile_tasks_length):
            arguments: list[str] = profile_tasks[i]
            command: str = arguments[0]
            
            if (command.__eq__("backup")):
                TaskHelper.backup(*arguments, logger_service = self.__logger_service)
            elif (command.__eq__("clear")):
                TaskHelper.clear(*arguments, logger_service = self.__logger_service)
            elif (command.__eq__("dialog")):
                TaskHelper.dialog(*arguments, widget_service = self.__widget_service)
            elif (command.__eq__("exit")):
                TaskHelper.exit(*arguments, logger_service = self.__logger_service)
            elif (command.__eq__("java")):
                parsed_arguments: list[str] = [
                    command,
                    basemodloader_filename,
                    arguments[1]
                ]
                
                TaskHelper.java(*parsed_arguments, logger_service = self.__logger_service)
            elif (command.__eq__("remove")):
                TaskHelper.remove(*arguments, logger_service = self.__logger_service)
            elif (command.__eq__("wget")):
                parsed_arguments: list[str] = [
                    command,
                    basemodloader_downloadurl,
                    data_basemodloader_file,
                    arguments[1],
                    arguments[2]
                ]

                TaskHelper.wget(*parsed_arguments)
        
        installedaddons: list[dict] = instance["installedAddons"]
        installedaddons_length: int = len(installedaddons)
        
        os.makedirs(data_mods_directory, exist_ok = True)

        for i in range(installedaddons_length):
            installedaddon: dict = installedaddons[i]
            
            installedfile_displayname: str = installedaddon["installedFile"]["displayName"]
            installedfile_downloadurl: str = installedaddon["installedFile"]["downloadUrl"]
            installedfile_filename: str = installedaddon["installedFile"]["fileName"]
            
            self.__logger_service.info_append(f"Installed File - Display Name: {installedfile_displayname}")
            self.__logger_service.info_append(f"Installed File - File Name: {installedfile_filename}")
            
            mods_installedaddon_file: str = os.path.join(data_mods_directory, installedfile_filename)
            
            HttpHelper.stream_download(installedfile_downloadurl, mods_installedaddon_file)
