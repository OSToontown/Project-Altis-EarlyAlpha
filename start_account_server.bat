@echo off

title Project Altis Account Server

set /P PPYTHON_PATH=<PPYTHON_PATH

%PPYTHON_PATH% accountserver/AccountServer.py
pause