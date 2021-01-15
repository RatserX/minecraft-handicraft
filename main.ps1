#Requires -RunAsAdministrator

# Configuration
$SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$WebClient = [System.Net.WebClient]::new()

$MajorSemVer = 3
$MinorSemVer = 9
$PatchSemVer = 1
$Version = "$MajorSemVer.$MinorSemVer.$PatchSemVer"

$FileNamePath = "$PSScriptRoot/python-$Version-amd64.exe"
$Address = "https://www.python.org/ftp/python/$Version/python-$Version-amd64.exe"
# TLS
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor $SecurityProtocol
# Python
if (!(Get-Package -Name "Python $MajorSemVer*")) {
    $WebClient.DownloadFile($Address, $FileNamePath)
    
    Start-Process -ArgumentList "/passive InstallAllUsers=1 PrependPath=1" -FilePath $FileNamePath -Wait
}
# Main
Set-Location -Path $PSScriptRoot

pip install -r "requirements.txt"
python "./src/main.py"
# Finish
Write-Host "Press any key to continue . . ."

$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
# Cleanup
Start-Sleep -Seconds 1
Remove-Item -Path $FileNamePath
