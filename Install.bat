@echo off
setlocal enabledelayedexpansion

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel%==0 (
    echo Python is already installed.
    python --version
    goto end
)

:: Python not installed
echo Python is not installed on this system.

:: Ask user if they want to install Python
set /p userChoice="Would you like to install Python 3.10? (Y/N): "
if /i "!userChoice!"=="Y" (
    echo Downloading Python 3.10 installer...
    
    :: Download Python installer
    curl -o python-installer.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe

    if exist python-installer.exe (
        echo Running the Python installer...
        
        :: Run the Python installer silently
        python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
        
        :: Check if installation was successful
        python --version >nul 2>&1
        if %errorlevel%==0 (
            echo Python 3.10 installed successfully.
            python --version
        ) else (
            echo Python installation failed. Please try manually installing it.
        )
        
        :: Clean up installer
        del python-installer.exe
    ) else (
        echo Failed to download the Python installer. Please check your internet connection.
    )
) else (
    echo Installation canceled by user.
)

:end

echo Installing Dependencies...

pip install -r requirements.txt

pause