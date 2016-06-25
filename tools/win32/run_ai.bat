:top
@echo off
title Toontown Two (AI Console)
cd ..\..\

dependencies\panda\python\ppython -m toontown.ai.AIStart
pause
goto top