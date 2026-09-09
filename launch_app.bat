@echo off
title Roblox Enterprise Suite Launcher

:: 1. IMMEDIATELY HIDE WINDOW
if "%~1"=="-invisible" goto :RUN_SUITE
mshta vbscript:Execute("CreateObject(""Wscript.Shell"").Run """"%~f0"" -invisible"",0:close")
exit

:RUN_SUITE
cd /d "%~dp0"

:: 2. SILENT ENVIRONMENT INSTALLER 
:: Fast downloads any missing packages for Python in the background
py -m pip install roblox fastapi uvicorn pydantic colorama --no-cache-dir --disable-pip-version-check --quiet

:: 3. SHUT DOWN INTERACTIVE TERMINAL TRACKS & OPEN APP
if exist main.py (
    start "" pyw main.py
)
exit