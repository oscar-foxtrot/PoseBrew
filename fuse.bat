@echo off
setlocal enabledelayedexpansion

REM Check required arguments
if "%~2"=="" (
    goto :usage
)

REM Default flags
set "npy_mode=0"
set "synced_flag="

REM Validate arguments
set "arg1=%~1"
set "arg2=%~2"

REM Loop over all args and parse flags
shift
shift
:parse_loop
if "%~1"=="" goto after_args
if /i "%~1"=="--npy" (
    set "npy_mode=1"
) else if /i "%~1"=="--synced" (
    set "synced_flag=--synced"
) else (
    echo Error: Unknown flag "%~1"
    goto :usage
)
shift
goto parse_loop

:after_args

call conda activate motionbert_env

if "%npy_mode%"=="1" (
    echo Skipping inference
    python python_files\fuse.py --input_1 "%arg1%" --input_2 "%arg2%" %synced_flag%
) else (
    echo Performing inference...
    call infer.bat "%arg1%"
    call infer.bat "%arg2%"
    python python_files\fuse.py --input_1 "predictions\%~n1.npy" --input_2 "predictions\%~n2.npy" %synced_flag%
)

call conda deactivate
exit /b 0

:usage
echo.
echo Usage: %~nx0 file1 file2 [--npy] [--synced]
echo Example: %~nx0 video1.mp4 video2.mp4
echo          %~nx0 file1.npy file2.npy --npy --synced
exit /b 1