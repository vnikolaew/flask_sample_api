$rootFolder = Split-Path -Parent $PSScriptRoot

Set-Location $rootFolder

$pythonExePath = ".venv\\Scripts\\python.exe"
$outFolder = "__generated__"

if(-not (Test-Path "$rootFolder/$outFolder")) {
    New-Item -Path "$rootFolder/$outFolder" -ItemType Directory
}

Invoke-Expression "$pythonExePath -m grpc_tools.protoc -I ./protos --python_out=./$outFolder --pyi_out=./$outFolder --grpc_python_out=./$outFolder ./protos/social_media.proto"