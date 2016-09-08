@echo off
cd ..

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttUsername="Username: "
set /P ttPassword="Password: "
set /P TT_GAMESERVER="Gameserver (DEFAULT: 127.0.0.1): " || ^
set TT_GAMESERVER=127.0.0.1

echo ===============================
echo Starting Project Altis...
echo ppython: %PPYTHON_PATH%
echo Username: %ttUsername%
echo Gameserver: %TT_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStartRemoteDB
pause
