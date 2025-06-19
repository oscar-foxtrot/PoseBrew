@echo off

REM In file names ALWAYS use backslashes (\) instead of forward slahses (/)

REM Check if an argument is provided
if "%~1"=="" (
    echo Usage: infer.bat filename.mp4
    exit /b
)

REM Extract argument
set "file_name=%~1"



REM Run MMPOSE inference
call conda activate openmmlab_env

python python_files\inf.py --input %file_name% --out_dir mmpose_output\output_%~n1

call conda deactivate



REM Run tracking
call conda activate boxmot_env

python python_files\bbox.py --input_video %file_name% ^
--input_json mmpose_output\output_%~n1\predictions\%~n1.json ^
--output_video boxmot_output\%~n1.mp4 ^
--output_json mmpose_output\output_%~n1\predictions\modified_%~n1.json

python python_files\intermediate_to_alpha.py --input_json mmpose_output\output_%~n1\predictions\modified_%~n1.json ^
--input_video %file_name% ^
--output_json_prefix mmpose_output\output_%~n1\predictions\%~n1

call conda deactivate



REM Run MotionBERT inference
call conda activate motionbert_env

set "FFMPEG_PATH=%CD%\ffmpeg\bin"
set PATH=%FFMPEG_PATH%;%PATH%

cd MotionBERT

copy /Y "..\%file_name%" "%~n1_0.mp4"
ffmpeg -y -i "..\%file_name%" -ss 00:00:02.700 -c:v libx264 -c:a aac "%~n1_1.mp4"
ffmpeg -y -i "..\%file_name%" -ss 00:00:05.400 -c:v libx264 -c:a aac "%~n1_2.mp4"

if not exist "..\motionbert_output" mkdir "..\motionbert_output"

REM Note that the output MUST be in the form of 3 videos suffixed _0, _1 and _2 to be correctly used at the following step
python infer_wild.py --vid_path %~n1_0.mp4 --json_path ..\mmpose_output\output_%~n1\predictions\%~n1_toalpha_0.json --out_path ..\motionbert_output\%~n1_0
python infer_wild.py --vid_path %~n1_1.mp4 --json_path ..\mmpose_output\output_%~n1\predictions\%~n1_toalpha_1.json --out_path ..\motionbert_output\%~n1_1
python infer_wild.py --vid_path %~n1_2.mp4 --json_path ..\mmpose_output\output_%~n1\predictions\%~n1_toalpha_2.json --out_path ..\motionbert_output\%~n1_2

del "%~n1_0.mp4"
del "%~n1_1.mp4"
del "%~n1_2.mp4"

cd ..

python python_files\ensemble.py --input_file_prefix motionbert_output\%~n1

call conda deactivate