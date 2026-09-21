@echo off
py -V:2.7 process_init.py
py -V:2.7 process_global_variables.py
py -V:2.7 process_scripts.py
@del *.pyc
echo.
echo ______________________________
echo.
echo Script processing has ended.
echo Press any key to exit. . .
pause>nul