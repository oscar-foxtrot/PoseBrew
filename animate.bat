@echo off

REM In file names ALWAYS use backslashes (\) instead of forward slahses (/)

REM Check if at least one argument is provided
if "%~1"=="" (
    echo Usage: animate.bat file1.npy [file2.npy]
    exit /b
)

call conda activate motionbert_env

REM Conditionally add --input_file_2
if "%~2"=="" (
    python python_files\animate.py --input_file_1 "%~1"
) else (
    python python_files\animate.py --input_file_1 "%~1" --input_file_2 "%~2"
)

call conda deactivate