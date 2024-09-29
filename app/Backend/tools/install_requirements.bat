@echo off
Title Requirements Installer

@echo Starting install_requirements.bat
@echo.

setlocal enabledelayedexpansion

set "installed="
set "skipped="

for /F "tokens=*" %%i in (../requirements.txt) do (
    @echo Installing %%i...
    pip install %%i
    IF ERRORLEVEL 1 (
        set "skipped=!skipped! %%i"
        @echo Failed to install %%i. Skipping...
    ) ELSE (
        set "installed=!installed! %%i"
        @echo Successfully installed %%i
    )
)

echo.
@echo =========================
@echo Summary of installations:
@echo =========================
echo.
@echo Newly Installed Libraries: 
if defined installed (
    echo !installed!
) else (
    echo None
)
echo.
@echo Skipped/Failed Libraries: 
if defined skipped (
    echo !skipped!
) else (
    echo None
)
echo.

TIMEOUT /T 7 /NOBREAK
