@ECHO OFF
cd ../..
echo "Updating git submodule..."
git submodule update
cd develop_scripts/submodule/
echo "Executing copying script.."
PowerShell.exe -file UpdateSubMOdule.ps1