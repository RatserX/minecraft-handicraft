@echo off

cls
cd %~dp0
call pip install -r "requirements.txt"
call python "./src/main.py"
pause
