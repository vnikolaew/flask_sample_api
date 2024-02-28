$rootFolder = Split-Path -Parent $PSScriptRoot

Set-Location $rootFolder

$pythonExePath = ".venv\\Scripts\\python.exe"
$outFolder = "__generated__"

if(-not (Test-Path "$rootFolder/$outFolder")) {
    New-Item -Path "$rootFolder/$outFolder" -ItemType Directory
} else {
    Remove-Item "$rootFolder\$outFolder\*.*"
}

$protoFiles = Get-ChildItem -Path ./protos -Filter *.proto -Recurse -File -Name
$protoFiles | ForEach-Object {
    Invoke-Expression "$pythonExePath -m grpc_tools.protoc -I./protos --python_out=./$outFolder --pyi_out=./$outFolder --grpc_python_out=./$outFolder ./protos/$_"
}