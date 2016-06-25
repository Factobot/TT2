:top
@echo off
title Toontown Two Auth Server Database
cd ..\..\
cd dependencies\mongo\AuthServerDB
..\bin\mongod.exe --dbpath .
pause
goto top