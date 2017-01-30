write-host "Starting ..." 
$toIgnore = ".git","README.md"
$scriptDirectory = $PSScriptRoot
cd ../..
$submoduleDirectory = "py_proj_submodule\"
$destinationDirectory = "./"
$files = get-childitem  -path $submoduleDirectory
try{
    foreach ($file in $files)
    {
       if ($file.Name -in $toIgnore){
            write-host "Found " $file.Name "Ignoring..."
       } 
       else{
        Copy-Item -path $file.FullName -dest $destinationDirectory -recurse -Force
       }
    }
    write-host "Removing submodule directory..."
    Remove-Item $submoduleDirectory -Recurse -Force
}catch [Exception]
{
    write-host "Exception has occured!" $_.Exception.Message
}