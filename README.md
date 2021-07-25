
# handicraft

> A tool to automate the setup of Minecraft launchers, loaders and mods

[![python-39-blue](https://img.shields.io/badge/python-v3.9-blue)](https://www.python.org/) [![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)

[![Buy me a coffee](https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg)](https://www.buymeacoffee.com/Ratser)

Tired of having to manually deal with the setup of all the necessary stuff to join your friend's Minecraft server? Not anymore!

Customize which components to download and install. Define which type of launcher to setup and use. Also, through a CurseForge Minecraft Instance configuration file you can select which loaders or mods to use.
Forge? Fabric? No problem!

 Share your configuration files with your friends so you can all get the same components!

![Handicraft](https://raw.githubusercontent.com/RatserX/ratserx.github.io/master/public/images/minecraft-instance-analyzer.gif)

## Prerequisites

*  [Python 3](https://www.python.org/downloads/) - Python is an interpreted, high-level and general-purpose programming language. The project already contains the Python Embeddable Package for 64-bits, so it's not mandatory on Windows.

**IMPORTANT: Check the options "Install launcher for all users (recommended)" and "Add Python to PATH", then select the "Install Now" button. Alternatively, select the "Customize installation" button, check the option "for all users (requires elevation)" when installing the Optional Features and continue the installation.**

*  [Visual C++ Redistributable for Visual Studio 2015](https://www.microsoft.com/en-us/download/details.aspx?id=48145) - The Visual C++ Redistributable Packages install run-time components that are required to run C++ applications built using Visual Studio 2015. This is only required on Windows since the embedded distribution does not include the Microsoft C Runtime.

## Install

1.  [Download](https://github.com/RatserX/handicraft/archive/main.zip) the main project.
2. Extract the package.
3. Run as administrator either `main.bat` on Windows, `main.sh` on Linux or manually run the required commands for every other case.
```shell
pip3 install -r "requirements.txt"
python "./src/main.py"
```
5. Follow the program instructions.

## Customization

 - **configuration** - This folder contains all the configuration files.
	 - **profile.json** - This file allows you to handle how the CurseForge Minecraft profile or `minecraftinstance.json` is processed.
	 - **launcher.json** - This file allows you to handle the setup of Minecraft launchers independently for each platform (Windows, MacOS, Linux).
	 - **autorun.json** - This file allows you to automatically run the program with a specific *launcher* or *profile* key. In case this file is deleted, the program will ask you for input.
 - **data** - This folder can store the downloaded files.
 - **log** - This folder stores all the generated log files.
 - **profile** - This folder is usually used to store the `minecraftinstance.json` files from CurseForge locally.

© RatserX
