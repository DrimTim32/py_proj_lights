$version = $args[0]
$clean = $args[1]
$coverage = $args[2]
$files = ".eggs","py_proj_lights.egg-info",".cache"
$dir = ".\"
$commands ="test"

$pythonScript = "setup.py"

if( -Not (Test-Path "$dir$pythonScript")){
   cd ..
   cd ..

}
write-host "Starting tests..."

#version choose
if($coverage -ne "no")
{
    write-host "Getting coverage "
    coverage erase
    if($version -eq 2){
        python2 -m coverage run ./setup.py test
    }
    elseif($version -eq 3){
        python -m coverage run ./setup.py test
    }
    else{
        python2 -m coverage run ./setup.py test
        python -m coverage run -a ./setup.py test
    }
    write-host "Generating coverage file..."
    coverage html
}
elseif($version -eq 2)
{
	write-host "Testing python 2"
	python2 $pythonScript $commands
}
elseif($version -eq 3)
{
	write-host "Testing python 3"
	python $pythonScript $commands
} 
else
{
	write-host "Testing python 2"
	python2 $pythonScript $commands
	write-host "Testing python 3"
	python $pythonScript  $commands
}


#cleaning
if($clean -eq "yes")
{
    write-host "Removing not tmp directories ..."
    foreach($file in $files){
        if(Test-Path "$dir$file"){
            Remove-Item -Force -Recurse "$dir$file"
        }
    }
    write-host "Clearing compiled python files ..."
    get-childitem ./ -include *.pyc -recurse | foreach ($_) {remove-item $_.fullname -recurse}
    get-childitem ./ -include *.egg -recurse | foreach ($_) {remove-item $_.fullname -recurse}
    get-childitem ./ -include __pycache__ -recurse | foreach ($_) {remove-item $_.fullname -recurse}
}
write-host "All done."