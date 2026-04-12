@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "PIPELINE_LAUNCHER=O:\999_IGNORE\TTS_Engines\TTS_Pipeline\LAUNCH_TTS.bat"
set "SERIES_DIR=%~dp0"
if "%SERIES_DIR:~-1%"=="\" set "SERIES_DIR=%SERIES_DIR:~0,-1%"

if not exist "%PIPELINE_LAUNCHER%" (
    echo [ERROR] Pipeline launcher not found:
    echo         %PIPELINE_LAUNCHER%
    pause
    exit /b 1
)

if not "%~1"=="" goto :handle_arg

echo.
echo ==============================================================
echo    SERIES TTS LAUNCHER
echo ==============================================================
echo    Folder: %SERIES_DIR%
echo.
echo    1. Current folder only
echo    2. Include subfolders (recursive)
echo    3. Cancel
echo.
set /p MODE_CHOICE=Choose 1, 2, or 3: 

if "%MODE_CHOICE%"=="1" (
    call :process_folder "%SERIES_DIR%" "0"
    goto :done
)
if "%MODE_CHOICE%"=="2" (
    call :process_folder "%SERIES_DIR%" "1"
    goto :done
)

echo [INFO] Cancelled.
goto :done

:handle_arg
if /I "%~x1"==".md" (
    call :process_file "%~f1"
    goto :done
)

if /I "%~x1"==".txt" (
    call :process_file "%~f1"
    goto :done
)

if exist "%~1\*" (
    echo.
    echo Target folder: %~f1
    echo.
    echo    1. Current folder only
    echo    2. Include subfolders (recursive)
    echo    3. Cancel
    echo.
    set /p MODE_CHOICE=Choose 1, 2, or 3: 

    if "%MODE_CHOICE%"=="1" (
        call :process_folder "%~f1" "0"
        goto :done
    )
    if "%MODE_CHOICE%"=="2" (
        call :process_folder "%~f1" "1"
        goto :done
    )

    echo [INFO] Cancelled.
    goto :done
)

echo [ERROR] Unsupported input. Drag in a .md file, .txt file, or folder.
goto :done

:process_folder
set "TARGET_DIR=%~1"
set "IS_RECURSIVE=%~2"
set "FOUND=0"

echo.
echo [INFO] Processing folder: %TARGET_DIR%
if "%IS_RECURSIVE%"=="1" (
    echo [INFO] Mode: recursive
    for /r "%TARGET_DIR%" %%F in (*.md *.txt) do (
        set "FOUND=1"
        call :process_file "%%~fF"
    )
) else (
    echo [INFO] Mode: current folder only
    for %%F in ("%TARGET_DIR%\*.md" "%TARGET_DIR%\*.txt") do (
        if exist "%%~fF" (
            set "FOUND=1"
            call :process_file "%%~fF"
        )
    )
)

if "!FOUND!"=="0" echo [INFO] No .md or .txt files found.
exit /b 0

:process_file
echo.
echo --------------------------------------------------------------
echo [FILE] %~f1
call "%PIPELINE_LAUNCHER%" "%~f1"
exit /b 0

:done
echo.
pause
exit /b 0
