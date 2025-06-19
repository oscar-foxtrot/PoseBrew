@echo off
setlocal

REM Download ffmpeg zip
powershell -Command "Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip'"

REM Extract ffmpeg zip
powershell -Command "Expand-Archive -LiteralPath 'ffmpeg.zip' -DestinationPath 'ffmpeg' -Force"

REM Delete zip
del ffmpeg.zip

REM Move bin folder to ffmpeg root and remove extras
for /d %%i in ("ffmpeg\ffmpeg-*-essentials*") do (
    move "%%i\bin" "ffmpeg"
    rmdir /s /q "%%i"
)