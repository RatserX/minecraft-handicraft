#Requires -RunAsAdministrator

# Configuration
$SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$WebClient = [System.Net.WebClient]::new()

$GetPipAddress = "https://bootstrap.pypa.io/get-pip.py"
$PythonVersion = "python-3.9.6-embed-amd64"

$BaseDirectory = Resolve-Path -Path $PSScriptRoot
$PythonDirectory = [IO.Path]::Combine($BaseDirectory, "..", $PythonVersion)
$GetPipFile = [IO.Path]::Combine($PythonDirectory, "get-pip.py")
$SiteCustomizeFile = [IO.Path]::Combine($PythonDirectory, "sitecustomize.py")
$PythonFile = [IO.Path]::Combine($PythonDirectory, "python.exe")
# TLS
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor $SecurityProtocol
# Site
$PythonPaths = Get-ChildItem -Filter "*._pth" -Path "$PythonDirectory"

foreach ($PythonPath in $PythonPaths) {
    $PathConfigurationFile = $PythonPath.FullName

    $PathConfigurationFileContent = Get-Content -Path "$PathConfigurationFile" -Raw
    $PathConfigurationFileValue = $PathConfigurationFileContent.Replace("#import", "import")

    Set-Content -Path "$PathConfigurationFile" -Value "$PathConfigurationFileValue"
}
# Site Customize
New-Item -Path $SiteCustomizeFile
Set-Content -Path $SiteCustomizeFile -Value "import site"
Add-Content -Path $SiteCustomizeFile -Value ""
Add-Content -Path $SiteCustomizeFile -Value "site.addsitedir(`"E:\.Development\minecraft-instance-analyzer\main\src`")"
# Pip
$WebClient.DownloadFile($GetPipAddress, $GetPipFile)

$GetPipFileContent = Get-Content -Path "$GetPipFile" -Raw
$GetPipFileValue = $GetPipFileContent.Replace("shutil.rmtree(tmpdir, ignore_errors=True)", "pass")

Set-Content -Path "$GetPipFile" -Value "$GetPipFileValue"
Start-Process -ArgumentList "$GetPipFile" -FilePath "$PythonFile" -Wait
# Finish
Write-Host "Press any key to continue . . ."

$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
# Cleanup
Start-Sleep -Seconds 1
Remove-Item -Path $GetPipFile
