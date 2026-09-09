@echo off
title Roblox Enterprise Bot Engine

:: 1. SECURELY HIDE THE BLACK WINDOW IMMEDIATELY
:: If the script wasn't launched invisibly, relaunch it using Windows silent background mode
if "%~1"=="-invisible" goto :RUN_ENGINE
mshta vbscript:Execute("CreateObject(""Wscript.Shell"").Run """"%~f0"" -invisible"",0:close")
exit

:RUN_ENGINE
:: Change directory directly to where this batch file is saved
cd /d "%~dp0"

:: 2. SILENT BACKGROUND PACKAGE DOWNLOADER
:: Installs the app requirements completely in the background with zero popups or prompts
py -m pip install roblox fastapi uvicorn pydantic colorama --no-cache-dir --disable-pip-version-check --quiet

:: 3. LAUNCH THE GRAPHICAL APP 
:: 'pyw' runs Python in "Windowed Mode", which completely bypasses the terminal console window
if exist main.py (
    start "" pyw main.py
)
exit
