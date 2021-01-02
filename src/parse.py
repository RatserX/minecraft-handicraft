#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections.abc
import os
import typing

import helper

class ParseProgress:
    def __init__(self, message: typing.Union[list[str], None], state: str):
        self.message: typing.Union[list[str], None] = message
        self.state: str = state

class ParseState:
    # Critical
    VALIDATE_CRITICAL_ADDON_DOWNLOAD_PROGRESS: str = "VALIDATE_CRITICAL_ADDON_DOWNLOAD_PROGRESS"

    # Info
    VALIDATE_INFO_ADDON_INSTALL_DRAFT: str = "VALIDATE_INFO_ADDON_INSTALL_DRAFT"
    VALIDATE_INFO_ADDON_INSTALL_OPTION: str = "VALIDATE_INFO_ADDON_INSTALL_OPTION"
    VALIDATE_INFO_INSTANCE_INSTALL_PATH: str = "VALIDATE_INFO_INSTANCE_INSTALL_PATH"
    VALIDATE_INFO_PLATFORM_DETAIL: str = "VALIDATE_INFO_PLATFORM_DETAIL"
    
    # Warn
    VALIDATE_WARN_ADDON_INSTALL_SKIP: str = "VALIDATE_WARN_ADDON_INSTALL_SKIP"

class Parse:
    def __init__(self, parse_option: dict):
        self.parse_option: dict = parse_option

    def download(self, parse_progress_callback: collections.abc.Callable[[ParseProgress], None] = None) -> None:
        base_mod_loader_date_modified: str = self.parse_option["baseModLoader"]["dateModified"]
        base_mod_loader_download_url: str = self.parse_option["baseModLoader"]["downloadUrl"]
        base_mod_loader_forge_version: str = self.parse_option["baseModLoader"]["forgeVersion"]
        base_mod_loader_minecraft_version: str = self.parse_option["baseModLoader"]["minecraftVersion"]

        parse_progress_callback(ParseProgress([
            f"{base_mod_loader_date_modified}",
            f"{base_mod_loader_download_url}",
            f"{base_mod_loader_forge_version}",
            f"{base_mod_loader_minecraft_version}"
        ], ParseState.VALIDATE_INFO_PLATFORM_DETAIL))
        
        install_path: str = self.parse_option["installPath"]
        name: str = self.parse_option["name"]
        installed_addons: list[dict] = self.parse_option["installedAddons"]

        instance_install_path: str = parse_progress_callback(ParseProgress([
            f"{install_path}",
            f"{name}"
        ], ParseState.VALIDATE_INFO_INSTANCE_INSTALL_PATH))

        addon_install_process: bool = False

        for installed_addon in installed_addons:
            installed_file_display_name: str = installed_addon["installedFile"]["displayName"]
            installed_file_download_url: str = installed_addon["installedFile"]["downloadUrl"]
            installed_file_file_date: str = installed_addon["installedFile"]["fileDate"]
            installed_file_file_name: str = installed_addon["installedFile"]["fileName"]

            addon_install_option: str = "Y"
            
            if (not addon_install_process):
                addon_install_option = parse_progress_callback(ParseProgress([
                    f"{installed_file_display_name}",
                    f"{installed_file_download_url}",
                    f"{installed_file_file_date}",
                    f"{installed_file_file_name}"
                ], ParseState.VALIDATE_INFO_ADDON_INSTALL_OPTION))
            
            if (addon_install_option == "A"):
                addon_install_option = "Y"
                addon_install_process = True
            
            if (addon_install_option == "N"):
                parse_progress_callback(ParseProgress([
                    f"{installed_file_display_name}",
                    f"{installed_file_download_url}",
                    f"{installed_file_file_date}",
                    f"{installed_file_file_name}"
                ], ParseState.VALIDATE_WARN_ADDON_INSTALL_SKIP))

                continue
            elif (addon_install_option == "Y"):
                parse_progress_callback(ParseProgress([
                    f"{installed_file_display_name}",
                    f"{installed_file_download_url}",
                    f"{installed_file_file_date}",
                    f"{installed_file_file_name}"
                ], ParseState.VALIDATE_INFO_ADDON_INSTALL_DRAFT))

                instance_install_file: str = os.path.join(instance_install_path, installed_file_file_name)

                try:
                    helper.Void.download_progress(instance_install_file, installed_file_download_url)
                except Exception as e:
                    message: str = e.args[0]

                    raise Exception(ParseProgress([
                        f"{message}",
                        f"{installed_file_display_name}",
                        f"{installed_file_download_url}",
                        f"{installed_file_file_date}",
                        f"{installed_file_file_name}"
                    ], ParseState.VALIDATE_CRITICAL_ADDON_DOWNLOAD_PROGRESS))
