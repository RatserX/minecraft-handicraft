#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections.abc
import re
import typing

class ParseProgress:
    def __init__(self, message: typing.Union[list[str], None], state: str):
        self.message: typing.Union[list[str], None] = message
        self.state: str = state

class ParseState:
    # Critical
    VALIDATE_CRITICAL_ROW_OVERFLOW: str = "VALIDATE_CRITICAL_ROW_OVERFLOW"

    # Info
    VALIDATE_INFO_ADDON_DETAIL: str = "VALIDATE_INFO_ADDON_DETAIL"
    VALIDATE_INFO_INSTANCE_DETAIL: str = "VALIDATE_INFO_INSTANCE_DETAIL"
    VALIDATE_INFO_PLATFORM_DETAIL: str = "VALIDATE_INFO_PLATFORM_DETAIL"

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

        parse_progress_callback(ParseProgress([
            f"{install_path}",
            f"{name}"
        ], ParseState.VALIDATE_INFO_INSTANCE_DETAIL))

        for installed_addon in installed_addons:
            installed_file_display_name: str = installed_addon["installedFile"]["displayName"]
            installed_file_download_url: str = installed_addon["installedFile"]["downloadUrl"]
            installed_file_file_date: str = installed_addon["installedFile"]["fileDate"]
            installed_file_file_name: str = installed_addon["installedFile"]["fileName"]
            
            parse_progress_callback(ParseProgress([
                f"{installed_file_display_name}",
                f"{installed_file_download_url}",
                f"{installed_file_file_date}",
                f"{installed_file_file_name}"
            ], ParseState.VALIDATE_INFO_ADDON_DETAIL))
