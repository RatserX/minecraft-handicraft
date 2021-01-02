#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import string
import typing
import requests
import validators

import helper
import logger
import parse

def main():
    base_path: str = os.path.dirname(__file__)
    
    parse_configuration_file: str = os.path.join(base_path, "../public/configuration/parse.json")
    file_public_path: str = os.path.join(base_path, "../public/file")
    log_public_path: str = os.path.join(base_path, "../public/log")
    profile_public_path: str = os.path.join(base_path, "../public/profile")

    logger_instance: logger.Logger = logger.Logger("logger")

    logger_instance.set_directory(log_public_path)
    logger_instance.set_level(logger.alog.INFO)
    
    with open(parse_configuration_file, "r") as fp:
        parse_option: dict = json.load(fp)
    
    profiles: list[dict] = parse_option["profiles"]
    profile_index: int = 0
    profile_length: int = len(profiles)

    if (profile_length > 0):
        logger_instance.info("Profiles:")
        
        for i in range(profile_length):
            profile: dict = profiles[i]
            name: str = profile["name"]
            
            logger_instance.info(f"[{i}] - {name}")
        
        while True:
            input_index: int = helper.Number.input_numeric(f"Select profile (Default '{profile_index}'): ", profile_length, 0, profile_index)

            if (input_index >= 0):
                profile_index = input_index

                break
            
            helper.Void.deprint()
            logger_instance.warn("Invalid profile")

    profile: dict = profiles[profile_index]
    location_template: string.Template = string.Template(profile["location"])
    location: str = location_template.substitute({
        "PROFILE_PUBLIC_PATH": profile_public_path
    })
    
    parse_option: dict = {}

    if (os.path.isfile(location)):
        location_file: str = os.path.join(profile_public_path, location)

        with open(location_file, "r") as fp:
            parse_option = json.load(fp)
    elif (validators.url(location)):
        with requests.get(location) as response:
            parse_option = response.json()
    
    def parse_progress_callback(parse_progress: parse.ParseProgress) -> typing.Union[str, None]:
        parse_progress_message: typing.Union[list[str], None] = parse_progress.message
        parse_progress_state: str = parse_progress.state
        
        if (parse_progress_state == parse.ParseState.VALIDATE_INFO_ADDON_INSTALL_DRAFT):
            installed_file_display_name: str = parse_progress_message[0]
            installed_file_download_url: str = parse_progress_message[1]
            installed_file_file_date: str = parse_progress_message[2]
            installed_file_file_name: str = parse_progress_message[3]
            
            logger_instance.info_append(f"Drafting addon installation . . .")
            logger_instance.info_append(f"Display name: {installed_file_display_name}")
            logger_instance.info_append(f"Download URL: {installed_file_download_url}")
            logger_instance.info_append(f"File date: {installed_file_file_date}")
            logger_instance.info_append(f"File name: {installed_file_file_name}")
        elif (parse_progress_state == parse.ParseState.VALIDATE_INFO_ADDON_INSTALL_OPTION):
            installed_file_display_name: str = parse_progress_message[0]
            installed_file_download_url: str = parse_progress_message[1]
            installed_file_file_date: str = parse_progress_message[2]
            installed_file_file_name: str = parse_progress_message[3]

            addon_install_option: str = None

            while True:
                input_addon_install_option: str = helper.String.input_option(f"Verifying addon '{installed_file_display_name}' (Y: Process installation; N: Skip installation; A: Install everything): ", ["A", "N", "Y"])

                if (input_addon_install_option is not None):
                    addon_install_option: str = input_addon_install_option.upper()

                    break
                
                helper.Void.deprint()
                logger_instance.warn("Invalid addon install option")
            
            logger_instance.info_append(f"--- ADDON ---")

            return addon_install_option
        elif (parse_progress_state == parse.ParseState.VALIDATE_INFO_INSTANCE_INSTALL_PATH):
            install_path: str = os.path.normpath(file_public_path)
            name: str = parse_progress_message[1]

            instance_install_path: str = os.path.normpath(install_path)

            while True:
                input_instance_install_path: str = helper.String.input_path(f"Select install path (Default '{install_path}'): ", instance_install_path)
                
                if (input_instance_install_path is not None):
                    instance_install_path = input_instance_install_path

                    break
                
                helper.Void.deprint()
                logger_instance.warn("Invalid instance install path")
            
            logger_instance.info_append(f"--- INSTANCE ---")
            logger_instance.info_append(f"Install path: {install_path}")
            logger_instance.info_append(f"Name: {name}")
            
            return instance_install_path
        elif (parse_progress_state == parse.ParseState.VALIDATE_INFO_LOADER_INSTALL_DRAFT):
            base_mod_loader_date_modified: str = parse_progress_message[0]
            base_mod_loader_download_url: str = parse_progress_message[1]
            base_mod_loader_file_name: str = parse_progress_message[2]
            base_mod_loader_forge_version: str = parse_progress_message[3]
            base_mod_loader_minecraft_version: str = parse_progress_message[4]
            base_mod_loader_name: str = parse_progress_message[5]
            
            logger_instance.info_append(f"Drafting loader installation . . .")
            logger_instance.info_append(f"Date Modified: {base_mod_loader_date_modified}")
            logger_instance.info_append(f"Download URL: {base_mod_loader_download_url}")
            logger_instance.info_append(f"File Name: {base_mod_loader_file_name}")
            logger_instance.info_append(f"Forge Version: {base_mod_loader_forge_version}")
            logger_instance.info_append(f"Minecraft Version: {base_mod_loader_minecraft_version}")
            logger_instance.info_append(f"Name: {base_mod_loader_name}")
        elif (parse_progress_state == parse.ParseState.VALIDATE_INFO_LOADER_INSTALL_OPTION):
            base_mod_loader_date_modified: str = parse_progress_message[0]
            base_mod_loader_download_url: str = parse_progress_message[1]
            base_mod_loader_file_name: str = parse_progress_message[2]
            base_mod_loader_forge_version: str = parse_progress_message[3]
            base_mod_loader_minecraft_version: str = parse_progress_message[4]
            base_mod_loader_name: str = parse_progress_message[5]
            
            loader_install_option: str = None

            while True:
                input_loader_install_option: str = helper.String.input_option(f"Verifying loader '{base_mod_loader_name}' (Y: Process installation; N: Skip installation; A: Install everything): ", ["A", "N", "Y"])

                if (input_loader_install_option is not None):
                    loader_install_option: str = input_loader_install_option.upper()

                    break
                
                helper.Void.deprint()
                logger_instance.warn("Invalid loader install option")
            
            logger_instance.info_append(f"--- LOADER ---")

            return loader_install_option
        elif (parse_progress_state == parse.ParseState.VALIDATE_WARN_ADDON_INSTALL_SKIP):
            installed_file_display_name: str = parse_progress_message[0]
            installed_file_download_url: str = parse_progress_message[1]
            installed_file_file_date: str = parse_progress_message[2]
            installed_file_file_name: str = parse_progress_message[3]
            
            logger_instance.warn_append(f"Skipping addon installation . . .")
        elif (parse_progress_state == parse.ParseState.VALIDATE_WARN_LOADER_INSTALL_SKIP):
            base_mod_loader_date_modified: str = parse_progress_message[0]
            base_mod_loader_download_url: str = parse_progress_message[1]
            base_mod_loader_file_name: str = parse_progress_message[2]
            base_mod_loader_forge_version: str = parse_progress_message[3]
            base_mod_loader_minecraft_version: str = parse_progress_message[4]
            base_mod_loader_name: str = parse_progress_message[5]
            
            logger_instance.warn_append(f"Skipping loader installation . . .")
        
        return None
    
    try:
        parse_instance = parse.Parse(parse_option)
        
        parse_instance.download(parse_progress_callback)
    except Exception as e:
        exception: parse.ParseProgress = e.args[0]
        exception_message: typing.Union[list[str], None] = exception.message
        exception_state: str = exception.state

        if (exception_state == parse.ParseState.VALIDATE_CRITICAL_ADDON_DOWNLOAD_PROGRESS):
            message: str = exception_message[0]
            installed_file_display_name: str = exception_message[1]
            installed_file_download_url: str = exception_message[2]
            installed_file_file_date: str = exception_message[3]
            installed_file_file_name: str = exception_message[4]
            
            logger_instance.critical_append(f"Cannot download file", f"Message: {message}", f"Display Name: {installed_file_display_name}", f"Download URL: {installed_file_download_url}", f"File Date: {installed_file_file_date}", f"File Name: {installed_file_file_name}")
        elif (exception_state == parse.ParseState.VALIDATE_CRITICAL_LOADER_DOWNLOAD_PROGRESS):
            message: str = exception_message[0]
            base_mod_loader_date_modified: str = exception_message[1]
            base_mod_loader_download_url: str = exception_message[2]
            base_mod_loader_file_name: str = exception_message[3]
            base_mod_loader_forge_version: str = exception_message[4]
            base_mod_loader_minecraft_version: str = exception_message[5]
            base_mod_loader_name: str = exception_message[6]
            
            logger_instance.critical_append(f"Cannot download file", f"Message: {message}", f"Date Modified: {base_mod_loader_date_modified}", f"Download URL: {base_mod_loader_download_url}", f"File Name: {base_mod_loader_file_name}", f"Forge Version: {base_mod_loader_forge_version}", f"Minecraft Version: {base_mod_loader_minecraft_version}", f"Name: {base_mod_loader_name}")

main()
