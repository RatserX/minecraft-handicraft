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
            logger_instance.info("Invalid profile")

    profile: dict = profiles[profile_index]
    location_template: string.Template = string.Template(profile["location"])

    location_template.substitute({
        "FILE_PUBLIC_PATH": file_public_path
    })

    location = location_template.template
    parse_option: dict = {}

    if (os.path.isfile(location)):
        location_file: str = os.path.join(profile_public_path, location)

        with open(location_file, "r") as fp:
            parse_option = json.load(fp)
    elif (validators.url(location)):
        with requests.get(location) as response:
            parse_option = response.json()
    
    def parse_progress_callback(parse_progress: parse.ParseProgress):
        parse_progress_message: typing.Union[list[str], None] = parse_progress.message
        parse_progress_state: str = parse_progress.state

        pattern = r"\|"

        if (parse_progress_state == parse.ParseState.VALIDATE_INFO_ADDON_DETAIL):
            installed_file_display_name: str = parse_progress_message[0]
            installed_file_download_url: str = parse_progress_message[1]
            installed_file_file_date: str = parse_progress_message[2]
            installed_file_file_name: str = parse_progress_message[3]

            logger_instance.info_append(f"--- ADDON ---")
            logger_instance.info_append(f"Display name: {installed_file_display_name}")
            logger_instance.info_append(f"Download URL: {installed_file_download_url}")
            logger_instance.info_append(f"File date: {installed_file_file_date}")
            logger_instance.info_append(f"File name: {installed_file_file_name}")
        elif (parse_progress_state == parse.ParseState.VALIDATE_INFO_INSTANCE_DETAIL):
            install_path: str = parse_progress_message[0]
            name: str = parse_progress_message[1]

            while True:
                input_path: str = helper.String.input_path(f"Select install path (Default '{install_path}'): ", install_path)
                
                if (input_path is not None):
                    install_path = input_path

                    break
                
                helper.Void.deprint()
                logger_instance.info("Invalid install path")
            
            logger_instance.info_append(f"--- INSTANCE ---")
            logger_instance.info_append(f"Install path: {install_path}")
            logger_instance.info_append(f"Name: {name}")
        elif (parse_progress_state == parse.ParseState.VALIDATE_INFO_PLATFORM_DETAIL):
            base_mod_loader_date_modified: str = parse_progress_message[0]
            base_mod_loader_download_url: str = parse_progress_message[1]
            base_mod_loader_forge_version: str = parse_progress_message[2]
            base_mod_loader_minecraft_version: str = parse_progress_message[3]
            
            logger_instance.info_append(f"--- PLATFORM ---")
            logger_instance.info_append(f"Date modified: {base_mod_loader_date_modified}")
            logger_instance.info_append(f"Download URL: {base_mod_loader_download_url}")
            logger_instance.info_append(f"Forge version: {base_mod_loader_forge_version}")
            logger_instance.info_append(f"Minecraft version: {base_mod_loader_minecraft_version}")
    
    try:
        parse_instance = parse.Parse(parse_option)
        
        parse_instance.download(parse_progress_callback)
    except Exception as e:
        exception: parse.ParseProgress = e.args[0]
        exception_message: typing.Union[list[str], None] = exception.message
        exception_state: str = exception.state

main()
