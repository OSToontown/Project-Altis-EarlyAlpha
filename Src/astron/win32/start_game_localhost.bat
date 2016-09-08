@echo off
cd ../../

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttUsername="Username: "

rem Export the environment variables:
set ttPassword=password
set TT_PLAYCOOKIE=%ttUsername%
set TT_GAMESERVER=127.0.0.1

echo ===============================
echo Starting Project Altis...
echo ppython: %PPYTHON_PATH%
echo Username: %ttUsername%
echo Gameserver: %TT_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStart
pause
