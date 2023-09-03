@echo off
REM check if python 32/64 bit versions are installed

py -3.11-32 --version > nul 2>&1
if %errorlevel% neq 0 (
    echo python 3.11 32 bit version is not installed.
    echo Press any key to exit...
    pause >nul
    exit /b
)

py -3.11-64 --version > nul 2>&1
if %errorlevel% neq 0 (
    echo python 3.11 64 bit version is not installed.
    echo Press any key to exit...
    pause >nul
    exit /b
)

Pushd "%~dp0"
echo .
echo ........................................
echo SuperSimpleMH Run Manager
echo ........................................
echo .
echo .
echo PRESS one of the following options then press ENTER.
echo .
echo 1 - Install env
echo 2 - Run SuperSimpleMH
echo .
echo .
SET /P M=Type 1, 2 then press ENTER:
if %M% == 1 (
    if exist rpyc-d2-map-api\venv (
        echo Reinstalling env for rpyc-d2-map-api module...
        rmdir /s /q "rpyc-d2-map-api\venv"
    )

    cd rpyc-d2-map-api
    py -3.11-32 -m venv venv
    call .\venv\Scripts\activate
    pip install .
    echo rpyc-d2-map-api env installed successfully.
    call deactivate
    cd ..

    if exist venv (
        echo Reinstalling env for SuperSimpleMH module...
        rmdir /s /q "venv"
    )

    py -3.11-64 -m venv venv
    call .\venv\Scripts\activate
    pip install .
    call deactivate
    echo SuperSimpleMH env installed successfully.
    echo Installation complete.
    echo Press any key to exit...
    pause >nul
    exit /b
)

if %M% == 2 (
    if not exist rpyc-d2-map-api\venv (
        echo Please install env before running SuperSimpleMH.
        echo Press any key to exit...
        pause >nul
        exit /b
    )

    if not exist venv (
        echo Please install env before running SuperSimpleMH.
        echo Press any key to exit...
        pause >nul
        exit /b
    )

    call .\venv\Scripts\activate
    super_simple_mh
)
