@echo off
py -V:2.7 process_particle_sys.py
@del *.pyc
echo.
echo ______________________________
echo.
echo Script processing has ended.
echo Press any key to exit. . .
pause>nul