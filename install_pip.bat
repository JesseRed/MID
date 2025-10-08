@echo off
echo Installing pip for portable Python...
echo.

REM Download get-pip.py
echo Downloading get-pip.py...
powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'get-pip.py'"

REM Install pip
echo Installing pip...
python get-pip.py

REM Clean up
del get-pip.py

echo.
echo Pip installation complete!
echo Now you can run: pip install psychopy pyyaml
pause
