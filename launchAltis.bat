@echo off

title Project Altis

set /P PPYTHON_PATH=<PPYTHON_PATH
set ttUsername=%1
set ttPassword=%2

%PPYTHON_PATH% -m toontown.launcher.main
pause