import re
import subprocess
import time
import typing
import urllib.parse

from helpers.dictionary_helper import DictionaryHelper
from helpers.http_helper import HttpHelper
from helpers.inspect_helper import InspectHelper
from helpers.list_helper import ListHelper
from helpers.path_helper import PathHelper
from helpers.subprocess_helper import SubprocessHelper
from helpers.zipfile_helper import ZipfileHelper
from stores.execution_store import ExecutionStore
from services.logger_service import LoggerService
from services.widget_service import WidgetService

class TaskHelper:
    def backup(*args: typing.Any, logger_service: LoggerService) -> None:
        backup_path: str = args[1]
        
        task_directory: str = ExecutionStore.directory
        task_time: float = time.time()
        
        if (PathHelper.exists(task_directory, backup_path)):
            task_src: str = PathHelper.get_directory_glob(task_directory, backup_path)
            task_dst: str = ""
            
            if (task_src != None):
                task_dst = f"{task_src}.{task_time}"
            else:
                task_src = PathHelper.get_file_glob(task_directory, backup_path)
                task_dst = f"{task_src}.{task_time}.miab"
            
            PathHelper.copy(task_src, task_dst)
            logger_service.info_append(f"'{InspectHelper.get_function_name()}' task succeeded. Path: '{backup_path}'.")
        else:
            logger_service.warn_append(f"'{InspectHelper.get_function_name()}' task failed. Path does not exists.")
    
    def clear(*args: typing.Any, logger_service: LoggerService) -> None:
        clear_path: str = args[1]
        
        task_directory: str = ExecutionStore.directory
        task_path: str = PathHelper.get_directory_glob(task_directory, clear_path)

        if (PathHelper.clear(task_path)):
            logger_service.info_append(f"'{InspectHelper.get_function_name()}' task succeeded. Path: '{clear_path}'.")
        else:
            logger_service.warn_append(f"'{InspectHelper.get_function_name()}' task failed. Path does not exists.")
    
    def call(*args: typing.Any, logger_service: LoggerService) -> None:
        call_parameters: tuple = args[4:]
        call_timeout: int = ListHelper.get(args, 3)
        call_key: str = args[2]
        call_file: str = PathHelper.get_file_path(args[1], extension = True)

        task_directory: str = ExecutionStore.directory
        task_subprocesses: dict[str, subprocess.Popen] = ExecutionStore.subprocesses
        
        task_timeout = int(call_timeout) if (call_timeout != None) else None
        task_path: str = PathHelper.get_file_glob(task_directory, call_file)
        task_parameters: list[str] = list(call_parameters)
        task_args: list[str] = [task_path] + task_parameters
        
        if (not DictionaryHelper.has(task_subprocesses, call_key)):
            ExecutionStore.subprocesses[call_key] = SubprocessHelper.popen(*task_args, timeout = task_timeout)
            
            logger_service.info_append(f"'{InspectHelper.get_function_name()}' task succeeded. Subprocess: '{call_key}'.")
        else:
            logger_service.warn_append(f"'{InspectHelper.get_function_name()}' task failed. Subprocess already exists.")
            #raise KeyError(f"Call key already exists: {call_key}")
    
    def cd(*args: typing.Any) -> None:
        cd_path: str = args[1]

        task_directory = ExecutionStore.directory
        ExecutionStore.directory = PathHelper.get_directory_glob(task_directory, cd_path)
    
    def exit(*args: typing.Any, logger_service: LoggerService) -> None:
        exit_key: str = args[1]

        task_subprocesses: dict[str, subprocess.Popen] = ExecutionStore.subprocesses

        if (DictionaryHelper.has(task_subprocesses, exit_key)):
            task_subprocess: subprocess.Popen = task_subprocesses[exit_key]

            if (task_subprocess != None):
                task_subprocess.terminate()
                task_subprocess.wait()
            
            del ExecutionStore.subprocesses[exit_key]
            logger_service.info_append(f"'{InspectHelper.get_function_name()}' task succeeded. Subprocess: '{exit_key}'.")
        else:
            logger_service.warn_append(f"'{InspectHelper.get_function_name()}' task failed. Subprocess does not exists.")
    
    def java(*args: typing.Any, logger_service: LoggerService) -> None:
        java_timeout: int = ListHelper.get(args, 3)
        java_key: str = args[2]
        java_file: str = PathHelper.get_file_path(args[1], extension = True)

        task_directory: str = ExecutionStore.directory
        task_subprocesses: dict[str, subprocess.Popen] = ExecutionStore.subprocesses
        
        task_timeout = int(java_timeout) if (java_timeout != None) else None
        task_path: str = PathHelper.get_file_glob(task_directory, java_file)
        task_args: list[str] = ["java", "-jar", task_path]
        
        if (not DictionaryHelper.has(task_subprocesses, java_key)):
            ExecutionStore.subprocesses[java_key] = SubprocessHelper.popen(*task_args, timeout = task_timeout)
            
            logger_service.info_append(f"'{InspectHelper.get_function_name()}' task succeeded. File: '{java_file}'.")
        else:
            logger_service.warn_append(f"'{InspectHelper.get_function_name()}' task failed. Subprocess already exists.")
            #raise KeyError(f"Java key already exists: {java_key}")
    
    def modal(*args: typing.Any, widget_service: WidgetService) -> None:
        modal_messages: tuple = args[3:]
        modal_header: tuple = args[2]
        modal_caption: tuple = args[1]
        
        task_messages: list[str] = [f"{modal_header}\n"] + list(modal_messages)
        task_message: str = "\n".join(task_messages)
        task_parsed_message: str = re.sub(r"[^\S\n]+", " ", task_message)
        task_caption: str = modal_caption

        widget_service.modal(None, task_parsed_message, task_caption)
    
    def remove(*args: typing.Any, logger_service: LoggerService) -> None:
        remove_path: str = args[1]
        
        task_directory: str = ExecutionStore.directory
        task_path: str = PathHelper.get_file_glob(task_directory, remove_path)

        if (PathHelper.remove(task_path)):
            logger_service.info_append(f"'{InspectHelper.get_function_name()}' task succeeded. Path: '{remove_path}'.")
        else:
            logger_service.warn_append(f"'{InspectHelper.get_function_name()}' task failed. Path does not exists.")
    
    def unzip(*args: typing.Any, logger_service: LoggerService) -> None:
        unzip_file: str = PathHelper.get_file_path(args[1], extension = True)
        
        task_directory: str = ExecutionStore.directory
        task_file: str = PathHelper.get_file_glob(task_directory, unzip_file)
        task_path: str = PathHelper.get_file_path(task_file, directory = True)

        ZipfileHelper.extractall(task_file, task_path)
        logger_service.info_append(f"'{InspectHelper.get_function_name()}' task completed. File: '{unzip_file}'.")
    
    def wget(*args: typing.Any) -> None:
        wget_repl: str = ListHelper.get(args, 4)
        wget_pattern: str = ListHelper.get(args, 3)
        wget_file: str = PathHelper.get_file_path(args[2], extension = True)
        wget_url: str = re.sub(wget_pattern, wget_repl, args[1]) if (wget_pattern != None) else args[1]
        
        task_directory: str = ExecutionStore.directory
        task_file: str = PathHelper.join(task_directory, wget_file)
        
        task_urlparse: urllib.parse.ParseResult = urllib.parse.urlparse(wget_url)
        task_url: str = task_urlparse.geturl()

        HttpHelper.stream_download(task_url, task_file)
