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
    VALIDATE_CRITICAL_LOADER_DOWNLOAD_PROGRESS: str = "VALIDATE_CRITICAL_LOADER_DOWNLOAD_PROGRESS"

    # Info
    VALIDATE_INFO_ADDON_INSTALL_DRAFT: str = "VALIDATE_INFO_ADDON_INSTALL_DRAFT"
    VALIDATE_INFO_ADDON_INSTALL_OPTION: str = "VALIDATE_INFO_ADDON_INSTALL_OPTION"
    VALIDATE_INFO_INSTANCE_INSTALL_PATH: str = "VALIDATE_INFO_INSTANCE_INSTALL_PATH"
    VALIDATE_INFO_LOADER_INSTALL_DRAFT: str = "VALIDATE_INFO_LOADER_INSTALL_DRAFT"
    VALIDATE_INFO_LOADER_INSTALL_OPTION: str = "VALIDATE_INFO_LOADER_INSTALL_OPTION"
    
    # Warn
    VALIDATE_WARN_ADDON_INSTALL_SKIP: str = "VALIDATE_WARN_ADDON_INSTALL_SKIP"
    VALIDATE_WARN_LOADER_INSTALL_SKIP: str = "VALIDATE_WARN_LOADER_INSTALL_SKIP"

class Parse:
    def __init__(self, parse_option: dict):
        self.parse_option: dict = parse_option

    def download(self, parse_progress_callback: collections.abc.Callable[[ParseProgress], None] = None) -> None:
        install_path: str = self.parse_option["installPath"]
        name: str = self.parse_option["name"]
        installed_addons: list[dict] = self.parse_option["installedAddons"]

        instance_install_path: str = parse_progress_callback(ParseProgress([
            f"{install_path}",
            f"{name}"
        ], ParseState.VALIDATE_INFO_INSTANCE_INSTALL_PATH))

        base_mod_loader_date_modified: str = self.parse_option["baseModLoader"]["dateModified"]
        base_mod_loader_download_url: str = self.parse_option["baseModLoader"]["downloadUrl"]
        base_mod_loader_file_name: str = self.parse_option["baseModLoader"]["filename"]
        base_mod_loader_forge_version: str = self.parse_option["baseModLoader"]["forgeVersion"]
        base_mod_loader_minecraft_version: str = self.parse_option["baseModLoader"]["minecraftVersion"]
        base_mod_loader_name: str = self.parse_option["baseModLoader"]["name"]
        
        install_process: bool = False
        loader_install_option: str = "Y"

        if (not install_process):
            loader_install_option = parse_progress_callback(ParseProgress([
                f"{base_mod_loader_date_modified}",
                f"{base_mod_loader_download_url}",
                f"{base_mod_loader_file_name}",
                f"{base_mod_loader_forge_version}",
                f"{base_mod_loader_minecraft_version}",
                f"{base_mod_loader_name}"
            ], ParseState.VALIDATE_INFO_LOADER_INSTALL_OPTION))
            
            if (loader_install_option == "A"):
                install_process = True
                loader_install_option = "Y"
            
            if (loader_install_option == "N"):
                parse_progress_callback(ParseProgress([
                    f"{base_mod_loader_date_modified}",
                    f"{base_mod_loader_download_url}",
                    f"{base_mod_loader_file_name}",
                    f"{base_mod_loader_forge_version}",
                    f"{base_mod_loader_minecraft_version}",
                    f"{base_mod_loader_name}"
                ], ParseState.VALIDATE_WARN_LOADER_INSTALL_SKIP))
            elif (loader_install_option == "Y"):
                parse_progress_callback(ParseProgress([
                    f"{base_mod_loader_date_modified}",
                    f"{base_mod_loader_download_url}",
                    f"{base_mod_loader_file_name}",
                    f"{base_mod_loader_forge_version}",
                    f"{base_mod_loader_minecraft_version}",
                    f"{base_mod_loader_name}"
                ], ParseState.VALIDATE_INFO_LOADER_INSTALL_DRAFT))
                
                loader_install_path: str = os.path.normpath(instance_install_path)
                loader_install_file: str = os.path.join(loader_install_path, base_mod_loader_file_name)

                try:
                    os.makedirs(loader_install_path, exist_ok=True)
                    helper.Void.download_progress(loader_install_file, base_mod_loader_download_url)
                except Exception as e:
                    message: str = e.args[0]

                    raise Exception(ParseProgress([
                        f"{message}",
                        f"{base_mod_loader_date_modified}",
                        f"{base_mod_loader_download_url}",
                        f"{base_mod_loader_file_name}",
                        f"{base_mod_loader_forge_version}",
                        f"{base_mod_loader_minecraft_version}",
                        f"{base_mod_loader_name}"
                    ], ParseState.VALIDATE_CRITICAL_LOADER_DOWNLOAD_PROGRESS))

        for installed_addon in installed_addons:
            installed_file_display_name: str = installed_addon["installedFile"]["displayName"]
            installed_file_download_url: str = installed_addon["installedFile"]["downloadUrl"]
            installed_file_file_date: str = installed_addon["installedFile"]["fileDate"]
            installed_file_file_name: str = installed_addon["installedFile"]["fileName"]

            addon_install_option: str = "Y"
            
            if (not install_process):
                addon_install_option = parse_progress_callback(ParseProgress([
                    f"{installed_file_display_name}",
                    f"{installed_file_download_url}",
                    f"{installed_file_file_date}",
                    f"{installed_file_file_name}"
                ], ParseState.VALIDATE_INFO_ADDON_INSTALL_OPTION))
            
            if (addon_install_option == "A"):
                install_process = True
                addon_install_option = "Y"
            
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

                addon_install_path: str = os.path.join(instance_install_path, "mods")
                addon_install_file: str = os.path.join(addon_install_path, installed_file_file_name)

                try:
                    os.makedirs(addon_install_path, exist_ok=True)
                    helper.Void.download_progress(addon_install_file, installed_file_download_url)
                except Exception as e:
                    message: str = e.args[0]

                    raise Exception(ParseProgress([
                        f"{message}",
                        f"{installed_file_display_name}",
                        f"{installed_file_download_url}",
                        f"{installed_file_file_date}",
                        f"{installed_file_file_name}"
                    ], ParseState.VALIDATE_CRITICAL_ADDON_DOWNLOAD_PROGRESS))
