test.bat executes all tests
assuming there are two environment variables, python and python2
python is src to python.exe with python 3 version
python2 is src to python.exe with python 2 version

user can specify what python version ( 2 or 3 ) will execute scripts, if not provided both are testing

-nc
 with this switch script does not clean temporary files
-cov
 generates coverage files, if no python version is specified coverage is being generated for both versions and merged

Example:
test.bat 3 -nc
will test against python 3 and will not clean afterwards

test.bat 2
will test against python 2 and will clean temp files

test.bat 2 -cov
will generate coverage for python2

test.bat -cov -nc
will generate ONE coverage for both python versions and will clean temp files