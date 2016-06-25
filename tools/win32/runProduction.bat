:top
@echo off
set ACCOUNT_PLAYTOKEN=dev
set ACCOUNT_PASSWORD=12345
set OTPKey=AAAAA
title Toontown Two (Production Test Console)
cd ..\..\
dependencies\panda\python\ppython prodMain.py
pause
goto top