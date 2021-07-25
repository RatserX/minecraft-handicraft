#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import os

from helpers.io_helper import IoHelper
from scripts.configuration_script import ConfigurationScript
from scripts.execution_script import ExecutionScript
from services.logger_service import LoggerService, alog
from services.widget_service import WidgetService
from stores.configuration_store import ConfigurationStore
from stores.execution_store import ExecutionStore
from stores.path_store import PathStore

def main():
    PathStore.base_directory = os.path.dirname(__file__)
    PathStore.home_directory = pathlib.Path.home()
    
    public_configuration_directory: str = PathStore.get_public_configuration_directory()
    public_log_directory: str = PathStore.get_public_log_directory()

    configuration_autorun_file: str = os.path.join(public_configuration_directory, "autorun.json")
    configuration_launcher_file: str = os.path.join(public_configuration_directory, "launcher.json")
    configuration_profile_file: str = os.path.join(public_configuration_directory, "profile.json")
    
    logger_service: LoggerService = LoggerService("logger")
    widget_service: WidgetService = WidgetService()
    
    logger_service.set_directory(public_log_directory)
    logger_service.set_level(alog.INFO)

    try:
        ConfigurationStore.autorun = IoHelper.get_json(configuration_autorun_file, error = False)
        ConfigurationStore.launcher = IoHelper.get_json(configuration_launcher_file)
        ConfigurationStore.profile = IoHelper.get_json(configuration_profile_file)

        ExecutionStore.subprocesses = {}

        ConfigurationScript(logger_service)
        ExecutionScript(logger_service, widget_service)
    except Exception as e:
        if (hasattr(e, "args")):
            msg: list = list(e.args)
            logger_service.critical_append(*msg)
        else:
            raise e

main()
