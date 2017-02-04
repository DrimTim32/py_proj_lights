@ECHO OFF
cd ../develop_scripts/tests
call test.bat -cov
cd ../code_check
call code_check.bat -e f -f full_check
cd ../../docs