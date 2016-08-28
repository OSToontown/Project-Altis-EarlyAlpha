@echo off
cd "../../dependencies/astron/"

astrond --loglevel info config/cluster2.yml
pause
