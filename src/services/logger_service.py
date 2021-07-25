#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import time
import typing

import alog

class LoggerService:
    def __init__(self, name: str, category: str = "", directory: str = ""):
        alog_config: dict = alog.default_alog_config()
        
        self.__logger: alog.Alogger = alog.init_alogger(alog_config, name)
        
        self.__category: str = category
        self.__directory: str = directory
        self.__timestamp: float = time.time()
        
        self.__filehandler: typing.Union[logging.FileHandler, None] = None
    
    def add_filehandler(self):
        category: str = f"_{self.__category}" if self.__category else ""
        timestamp: str = str(self.__timestamp)

        filename: str = os.path.join(self.__directory, f"{timestamp}{category}.log")
        format = self.get_format()
        
        self.__filehandler = logging.FileHandler(filename, "a", "utf8")
        self.__filehandler.setFormatter(format)

        self.__logger.addHandler(self.__filehandler)
    
    def remove_filehandler(self):
        if (self.__filehandler is not None):
            self.__logger.removeHandler(self.__filehandler)

            self.__filehandler = None
    
    def get_category(self) -> str:
        return self.__category
    
    def set_category(self, category: str) -> None:
        self.__category = category
    
    def get_directory(self) -> str:
        return self.__directory
    
    def set_directory(self, directory: str) -> None:
        self.__directory = directory
    
    def get_format(self) -> typing.Union[typing.Any, logging.Formatter, None]:
        return self.__logger.get_formatter()
    
    def set_format(self, fs: str, is_default: bool = False, time_strfmt: str = "%Y-%m-%d %H:%M:%S") -> None:
        self.__logger.set_format(fs, self.__logger, is_default, time_strfmt)
    
    def get_level(self) -> typing.Any:
        return self.__logger.get_level()
    
    def set_level(self, level: typing.Union[int, str]) -> None:
        self.__logger.setLevel(level)
    
    def get_timestamp(self) -> float:
        return self.__timestamp
    
    def set_timestamp(self, timestamp: typing.Union[float, None] = None) -> None:
        if (timestamp is None):
            self.__timestamp = time.time()
        else:
            self.__timestamp = timestamp
    
    def critical(self, *msg: list[str]) -> None:
        message: str = ' '.join(msg)
        
        self.__logger.critical(message)
    
    def critical_append(self, *msg: list[str]) -> None:
        self.add_filehandler()
        self.critical(*msg)
        self.remove_filehandler()
    
    def debug(self, *msg: list[str]) -> None:
        message: str = ' '.join(msg)
        
        self.__logger.debug(message)
    
    def debug_append(self, *msg: list[str]) -> None:
        self.add_filehandler()
        self.debug(*msg)
        self.remove_filehandler()
    
    def error(self, *msg: list[str]) -> None:
        message: str = ' '.join(msg)
        
        self.__logger.error(message)
    
    def error_append(self, *msg: list[str]) -> None:
        self.add_filehandler()
        self.error(*msg)
        self.remove_filehandler()
    
    def info(self, *msg: list[str]) -> None:
        message: str = ' '.join(msg)
        
        self.__logger.info(message)
    
    def info_append(self, *msg: list[str]) -> None:
        self.add_filehandler()
        self.info(*msg)
        self.remove_filehandler()
    
    def warn(self, *msg: list[str]) -> None:
        message: str = ' '.join(msg)
        
        self.__logger.warn(message)
    
    def warn_append(self, *msg: list[str]) -> None:
        self.add_filehandler()
        self.warn(*msg)
        self.remove_filehandler()
