@echo off
title Roblox Enterprise Suite Launcher

if "%~1"=="-invisible" goto :RUN_SUITE
powershell -Command "Start-Process '%~f0' -ArgumentList '-invisible' -WindowStyle Hidden"
exit

:RUN_SUITE
cd /d "%~dp0"
py -m pip install roblox fastapi uvicorn pydantic colorama argon2-cffi PyJWT cryptography pyinstaller --no-cache-dir --disable-pip-version-check --quiet
if exist main.py (
    start "" pyw main.py
)
exit
