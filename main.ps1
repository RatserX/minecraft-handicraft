#Requires -RunAsAdministrator

# Configuration
$PythonVersion = "python-3.9.6-embed-amd64"

$BaseDirectory = Resolve-Path -Path $PSScriptRoot
$PythonDirectory = [IO.Path]::Combine($BaseDirectory, "bin", $PythonVersion)

$PipFile = [IO.Path]::Combine($PythonDirectory, "Scripts/pip.exe")
$PythonFile = [IO.Path]::Combine($PythonDirectory, "python.exe")
# Location
Set-Location -Path $BaseDirectory
# Pip
Start-Process -ArgumentList "install -r `"requirements.txt`"" -FilePath "$PipFile" -Wait
# Python
Start-Process -ArgumentList "./src/main.py" -FilePath "$PythonFile" -Wait
# Finish
Write-Host "Press any key to continue . . ."

$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
