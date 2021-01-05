#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections.abc
import os
import typing

import helper

class ParserProgress:
    def __init__(self, message: typing.Union[list[str], None], state: str):
        self.message: typing.Union[list[str], None] = message
        self.state: str = state

class ParserState:
    # Critical
    PARSER_CRITICAL_ADDON_DOWNLOAD_PROGRESS: str = "PARSER_CRITICAL_ADDON_DOWNLOAD_PROGRESS"
    PARSER_CRITICAL_LOADER_DOWNLOAD_PROGRESS: str = "PARSER_CRITICAL_LOADER_DOWNLOAD_PROGRESS"

    # Info
    PARSER_INFO_ADDON_INSTALL_DRAFT: str = "PARSER_INFO_ADDON_INSTALL_DRAFT"
    PARSER_INFO_ADDON_INSTALL_OPTION: str = "PARSER_INFO_ADDON_INSTALL_OPTION"
    PARSER_INFO_INSTANCE_INSTALL_PATH: str = "PARSER_INFO_INSTANCE_INSTALL_PATH"
    PARSER_INFO_LOADER_INSTALL_DRAFT: str = "PARSER_INFO_LOADER_INSTALL_DRAFT"
    PARSER_INFO_LOADER_INSTALL_OPTION: str = "PARSER_INFO_LOADER_INSTALL_OPTION"
    
    # Warn
    PARSER_WARN_ADDON_INSTALL_SKIP: str = "PARSER_WARN_ADDON_INSTALL_SKIP"
    PARSER_WARN_LOADER_INSTALL_SKIP: str = "PARSER_WARN_LOADER_INSTALL_SKIP"

class Parse:
    def __init__(self, parser_option: dict):
        self.parser_option: dict = parser_option

    def download(self, parser_progress_callback: collections.abc.Callable[[ParserProgress], None] = None) -> None:
        install_path: str = self.parser_option["installPath"]
        name: str = self.parser_option["name"]
        installed_addons: list[dict] = self.parser_option["installedAddons"]

        instance_install_path: str = parser_progress_callback(ParserProgress([
            f"{install_path}",
            f"{name}"
        ], ParserState.PARSER_INFO_INSTANCE_INSTALL_PATH))

        base_mod_loader_date_modified: str = self.parser_option["baseModLoader"]["dateModified"]
        base_mod_loader_download_url: str = self.parser_option["baseModLoader"]["downloadUrl"]
        base_mod_loader_file_name: str = self.parser_option["baseModLoader"]["filename"]
        base_mod_loader_forge_version: str = self.parser_option["baseModLoader"]["forgeVersion"]
        base_mod_loader_minecraft_version: str = self.parser_option["baseModLoader"]["minecraftVersion"]
        base_mod_loader_name: str = self.parser_option["baseModLoader"]["name"]
        
        install_process: bool = False
        loader_install_option: str = "Y"

        if (not install_process):
            loader_install_option = parser_progress_callback(ParserProgress([
                f"{base_mod_loader_date_modified}",
                f"{base_mod_loader_download_url}",
                f"{base_mod_loader_file_name}",
                f"{base_mod_loader_forge_version}",
                f"{base_mod_loader_minecraft_version}",
                f"{base_mod_loader_name}"
            ], ParserState.PARSER_INFO_LOADER_INSTALL_OPTION))
            
            if (loader_install_option == "A"):
                install_process = True
                loader_install_option = "Y"
            
            if (loader_install_option == "N"):
                parser_progress_callback(ParserProgress([
                    f"{base_mod_loader_date_modified}",
                    f"{base_mod_loader_download_url}",
                    f"{base_mod_loader_file_name}",
                    f"{base_mod_loader_forge_version}",
                    f"{base_mod_loader_minecraft_version}",
                    f"{base_mod_loader_name}"
                ], ParserState.PARSER_WARN_LOADER_INSTALL_SKIP))
            elif (loader_install_option == "Y"):
                parser_progress_callback(ParserProgress([
                    f"{base_mod_loader_date_modified}",
                    f"{base_mod_loader_download_url}",
                    f"{base_mod_loader_file_name}",
                    f"{base_mod_loader_forge_version}",
                    f"{base_mod_loader_minecraft_version}",
                    f"{base_mod_loader_name}"
                ], ParserState.PARSER_INFO_LOADER_INSTALL_DRAFT))
                
                loader_install_path: str = os.path.normpath(instance_install_path)
                loader_install_file: str = os.path.join(loader_install_path, base_mod_loader_file_name)

                try:
                    os.makedirs(loader_install_path, exist_ok=True)
                    helper.Void.download_progress(loader_install_file, base_mod_loader_download_url)
                except Exception as e:
                    message: str = e.args[0]

                    raise Exception(ParserProgress([
                        f"{message}",
                        f"{base_mod_loader_date_modified}",
                        f"{base_mod_loader_download_url}",
                        f"{base_mod_loader_file_name}",
                        f"{base_mod_loader_forge_version}",
                        f"{base_mod_loader_minecraft_version}",
                        f"{base_mod_loader_name}"
                    ], ParserState.PARSER_CRITICAL_LOADER_DOWNLOAD_PROGRESS))

        for installed_addon in installed_addons:
            installed_file_display_name: str = installed_addon["installedFile"]["displayName"]
            installed_file_download_url: str = installed_addon["installedFile"]["downloadUrl"]
            installed_file_file_date: str = installed_addon["installedFile"]["fileDate"]
            installed_file_file_name: str = installed_addon["installedFile"]["fileName"]

            addon_install_option: str = "Y"
            
            if (not install_process):
                addon_install_option = parser_progress_callback(ParserProgress([
                    f"{installed_file_display_name}",
                    f"{installed_file_download_url}",
                    f"{installed_file_file_date}",
                    f"{installed_file_file_name}"
                ], ParserState.PARSER_INFO_ADDON_INSTALL_OPTION))
            
            if (addon_install_option == "A"):
                install_process = True
                addon_install_option = "Y"
            
            if (addon_install_option == "N"):
                parser_progress_callback(ParserProgress([
                    f"{installed_file_display_name}",
                    f"{installed_file_download_url}",
                    f"{installed_file_file_date}",
                    f"{installed_file_file_name}"
                ], ParserState.PARSER_WARN_ADDON_INSTALL_SKIP))

                continue
            elif (addon_install_option == "Y"):
                parser_progress_callback(ParserProgress([
                    f"{installed_file_display_name}",
                    f"{installed_file_download_url}",
                    f"{installed_file_file_date}",
                    f"{installed_file_file_name}"
                ], ParserState.PARSER_INFO_ADDON_INSTALL_DRAFT))

                addon_install_path: str = os.path.join(instance_install_path, "mods")
                addon_install_file: str = os.path.join(addon_install_path, installed_file_file_name)

                try:
                    os.makedirs(addon_install_path, exist_ok=True)
                    helper.Void.download_progress(addon_install_file, installed_file_download_url)
                except Exception as e:
                    message: str = e.args[0]

                    raise Exception(ParserProgress([
                        f"{message}",
                        f"{installed_file_display_name}",
                        f"{installed_file_download_url}",
                        f"{installed_file_file_date}",
                        f"{installed_file_file_name}"
                    ], ParserState.PARSER_CRITICAL_ADDON_DOWNLOAD_PROGRESS))
