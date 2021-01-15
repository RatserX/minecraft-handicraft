#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections.abc
import os
import pathlib
import string
import typing

import helper

class AnalyzerProgress:
    def __init__(self, message: typing.Union[list[str], None], state: str):
        self.message: typing.Union[list[str], None] = message
        self.state: str = state

class AnalyzerState:
    # Critical
    ANALYZER_CRITICAL_ADDON_DOWNLOAD_PROGRESS: str = "ANALYZER_CRITICAL_ADDON_DOWNLOAD_PROGRESS"
    ANALYZER_CRITICAL_LOADER_DOWNLOAD_PROGRESS: str = "ANALYZER_CRITICAL_LOADER_DOWNLOAD_PROGRESS"

    # Info
    ANALYZER_INFO_ADDON_INSTALL_DRAFT: str = "ANALYZER_INFO_ADDON_INSTALL_DRAFT"
    ANALYZER_INFO_ADDON_INSTALL_OPTION: str = "ANALYZER_INFO_ADDON_INSTALL_OPTION"
    ANALYZER_INFO_INSTANCE_INSTALL_PATH: str = "ANALYZER_INFO_INSTANCE_INSTALL_PATH"
    ANALYZER_INFO_LOADER_INSTALL_DRAFT: str = "ANALYZER_INFO_LOADER_INSTALL_DRAFT"
    ANALYZER_INFO_LOADER_INSTALL_OPTION: str = "ANALYZER_INFO_LOADER_INSTALL_OPTION"
    
    # Warn
    ANALYZER_WARN_ADDON_INSTALL_SKIP: str = "ANALYZER_WARN_ADDON_INSTALL_SKIP"
    ANALYZER_WARN_LOADER_INSTALL_SKIP: str = "ANALYZER_WARN_LOADER_INSTALL_SKIP"

class Analyzer:
    def __init__(self, analyzer_option: dict, analyzer_instance: dict):
        self.analyzer_instance: dict = analyzer_instance
        self.analyzer_option: dict = analyzer_option

    def download(self, analyzer_progress_callback: collections.abc.Callable[[AnalyzerProgress], None] = None) -> None:
        install_path: str = self.analyzer_instance["installPath"]
        name: str = self.analyzer_instance["name"]
        installed_addons: list[dict] = self.analyzer_instance["installedAddons"]

        directory: dict = self.analyzer_option["directory"]
        directory_path: str = None

        if (helper.Boolean.is_linux()):
            directory_path = directory["linux"]
        elif (helper.Boolean.is_osx()):
            directory_path = directory["osx"]
        elif (helper.Boolean.is_windows()):
            directory_path = directory["windows"]
        
        if (directory_path is not None):
            directory_path_template: string.Template = string.Template(directory_path)
            directory_path = directory_path_template.substitute({
                "HOME": pathlib.Path.home()
            })
            
            if (os.path.exists(directory_path)):
                install_path = os.path.normpath(directory_path)
        else:
            install_path = os.path.normpath(install_path)

        instance_install_path: str = analyzer_progress_callback(AnalyzerProgress([
            f"{install_path}",
            f"{name}"
        ], AnalyzerState.ANALYZER_INFO_INSTANCE_INSTALL_PATH))

        base_mod_loader_date_modified: str = self.analyzer_instance["baseModLoader"]["dateModified"]
        base_mod_loader_download_url: str = self.analyzer_instance["baseModLoader"]["downloadUrl"]
        base_mod_loader_file_name: str = self.analyzer_instance["baseModLoader"]["filename"]
        base_mod_loader_forge_version: str = self.analyzer_instance["baseModLoader"]["forgeVersion"]
        base_mod_loader_minecraft_version: str = self.analyzer_instance["baseModLoader"]["minecraftVersion"]
        base_mod_loader_name: str = self.analyzer_instance["baseModLoader"]["name"]
        
        install_process: bool = False
        loader_install_option: str = "Y"

        if (not install_process):
            loader_install_option = analyzer_progress_callback(AnalyzerProgress([
                f"{base_mod_loader_date_modified}",
                f"{base_mod_loader_download_url}",
                f"{base_mod_loader_file_name}",
                f"{base_mod_loader_forge_version}",
                f"{base_mod_loader_minecraft_version}",
                f"{base_mod_loader_name}"
            ], AnalyzerState.ANALYZER_INFO_LOADER_INSTALL_OPTION))
            
            if (loader_install_option == "A"):
                install_process = True
                loader_install_option = "Y"
            
            if (loader_install_option == "N"):
                analyzer_progress_callback(AnalyzerProgress([
                    f"{base_mod_loader_date_modified}",
                    f"{base_mod_loader_download_url}",
                    f"{base_mod_loader_file_name}",
                    f"{base_mod_loader_forge_version}",
                    f"{base_mod_loader_minecraft_version}",
                    f"{base_mod_loader_name}"
                ], AnalyzerState.ANALYZER_WARN_LOADER_INSTALL_SKIP))
            elif (loader_install_option == "Y"):
                analyzer_progress_callback(AnalyzerProgress([
                    f"{base_mod_loader_date_modified}",
                    f"{base_mod_loader_download_url}",
                    f"{base_mod_loader_file_name}",
                    f"{base_mod_loader_forge_version}",
                    f"{base_mod_loader_minecraft_version}",
                    f"{base_mod_loader_name}"
                ], AnalyzerState.ANALYZER_INFO_LOADER_INSTALL_DRAFT))
                
                loader_install_path: str = os.path.normpath(instance_install_path)
                loader_install_file: str = os.path.join(loader_install_path, base_mod_loader_file_name)

                try:
                    os.makedirs(loader_install_path, exist_ok=True)
                    helper.Void.download_progress(loader_install_file, base_mod_loader_download_url)
                except Exception as e:
                    message: str = e.args[0]

                    raise Exception(AnalyzerProgress([
                        f"{message}",
                        f"{base_mod_loader_date_modified}",
                        f"{base_mod_loader_download_url}",
                        f"{base_mod_loader_file_name}",
                        f"{base_mod_loader_forge_version}",
                        f"{base_mod_loader_minecraft_version}",
                        f"{base_mod_loader_name}"
                    ], AnalyzerState.ANALYZER_CRITICAL_LOADER_DOWNLOAD_PROGRESS))

        for installed_addon in installed_addons:
            installed_file_display_name: str = installed_addon["installedFile"]["displayName"]
            installed_file_download_url: str = installed_addon["installedFile"]["downloadUrl"]
            installed_file_file_date: str = installed_addon["installedFile"]["fileDate"]
            installed_file_file_name: str = installed_addon["installedFile"]["fileName"]

            addon_install_option: str = "Y"
            
            if (not install_process):
                addon_install_option = analyzer_progress_callback(AnalyzerProgress([
                    f"{installed_file_display_name}",
                    f"{installed_file_download_url}",
                    f"{installed_file_file_date}",
                    f"{installed_file_file_name}"
                ], AnalyzerState.ANALYZER_INFO_ADDON_INSTALL_OPTION))
            
            if (addon_install_option == "A"):
                install_process = True
                addon_install_option = "Y"
            
            if (addon_install_option == "N"):
                analyzer_progress_callback(AnalyzerProgress([
                    f"{installed_file_display_name}",
                    f"{installed_file_download_url}",
                    f"{installed_file_file_date}",
                    f"{installed_file_file_name}"
                ], AnalyzerState.ANALYZER_WARN_ADDON_INSTALL_SKIP))

                continue
            elif (addon_install_option == "Y"):
                analyzer_progress_callback(AnalyzerProgress([
                    f"{installed_file_display_name}",
                    f"{installed_file_download_url}",
                    f"{installed_file_file_date}",
                    f"{installed_file_file_name}"
                ], AnalyzerState.ANALYZER_INFO_ADDON_INSTALL_DRAFT))

                addon_install_path: str = os.path.join(instance_install_path, "mods")
                addon_install_file: str = os.path.join(addon_install_path, installed_file_file_name)

                try:
                    os.makedirs(addon_install_path, exist_ok=True)
                    helper.Void.download_progress(addon_install_file, installed_file_download_url)
                except Exception as e:
                    message: str = e.args[0]

                    raise Exception(AnalyzerProgress([
                        f"{message}",
                        f"{installed_file_display_name}",
                        f"{installed_file_download_url}",
                        f"{installed_file_file_date}",
                        f"{installed_file_file_name}"
                    ], AnalyzerState.ANALYZER_CRITICAL_ADDON_DOWNLOAD_PROGRESS))
