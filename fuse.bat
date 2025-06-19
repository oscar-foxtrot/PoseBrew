@echo off

if "%~1"=="" (
    echo Usage: %~nx0 file1 file2 [--npy] [--synced]
    echo Example: %~nx0 video1.mp4 video2.mp4
    echo          %~nx0 file1.npy file2.npy --npy --synced
    goto :eof
)

call conda activate motionbert_env

REM Check third argument. If --npy then two .npy files must be provided. Otherwise provide two videos ("%~1" and "%~2")

if /i "%~3"=="--npy" (
    echo Skipping inference
    python python_files\fuse.py --input_1 "%~1" --input_2 "%~2" %4
) else (
    echo Performing inference...
    infer.bat "%~1"
    infer.bat "%~2"
    python python_files\fuse.py --input_1 "predictions\%~n1.npy" --input_2 "predictions\%~n2.npy" %4
)

call conda deactivate