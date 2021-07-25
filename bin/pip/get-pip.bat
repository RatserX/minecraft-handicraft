@echo off

cls
cd %~dp0
call powershell -ExecutionPolicy "Bypass" -File "%~dp0/%~n0.ps1" -NoExit -NoProfile
pause
