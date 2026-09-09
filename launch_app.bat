@echo off
title Roblox Enterprise Suite Launcher

:: 1. PURGE AND CONCEAL TERMINAL CONSOLE FRAME IMMEDIATELY via PowerShell
if "%~1"=="-invisible" goto :RUN_SUITE
powershell -Command "Start-Process '%~f0' -ArgumentList '-invisible' -WindowStyle Hidden"
exit

:RUN_SUITE
cd /d "%~dp0"

:: 2. BACKGROUND QUIET PIP PACKAGE DOWNLOADER
py -m pip install roblox fastapi uvicorn pydantic colorama --no-cache-dir --disable-pip-version-check --quiet

:: 3. SHUT DOWN CLI BUFFER TRACKS & LAUNCH THE GRAPHICAL APP 
if exist main.py (
    start "" pyw main.py
)
exit