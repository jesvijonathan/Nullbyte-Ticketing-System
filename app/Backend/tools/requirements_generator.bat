@echo off
Title Requirements Generator

@echo Powered by pipreqs
@echo.
@echo Started generate_requirements.bat
@echo.

@echo Installing pipreqs...
python -m pip install pipreqs
IF ERRORLEVEL 1 (
    @echo Failed to install pipreqs. Skipping...
    exit /b
)

@echo.
@echo Creating requirements list...
@echo.
pipreqs ../ --force
IF ERRORLEVEL 1 (
    @echo Failed to create requirements.txt. Skipping...
    exit /b
)

@echo.
@echo Done listing dependencies to "%cd%\..\requirements.txt"
@echo.

:: start notepad "%cd%\..\requirements.txt"

@REM
TIMEOUT /T 7 /NOBREAK
