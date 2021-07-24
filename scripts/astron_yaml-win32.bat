@echo off
cd "../dependencies/astron/"
title Project Altis Astron

:start
astrond --loglevel info config/astrond.yml
PAUSE
goto start
