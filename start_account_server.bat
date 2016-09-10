@echo off

title Project Altis Account Server

set /P PPYTHON_PATH=<PPYTHON_PATH

cd accountserver

%PPYTHON_PATH% AccountServer.py
pause