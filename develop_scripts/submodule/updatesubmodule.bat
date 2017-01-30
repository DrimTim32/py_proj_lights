@ECHO OFF
cd ../..
git submodule update
cd develop_scripts/submodule/
PowerShell.exe -file UpdateSubMOdule.ps1