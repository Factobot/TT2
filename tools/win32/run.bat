:top
@echo off
title Toontown Two (Play Game Console)
set ACCOUNT_PLAYTOKEN=dev
set ACCOUNT_PASSWORD=12345
cd ..\..\

dependencies\panda\python\ppython main.py
pause
goto top