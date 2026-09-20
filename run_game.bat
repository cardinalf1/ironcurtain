@echo off
title The Iron Curtain - Cold War Simulation Platform
echo ===============================================================================
echo   THE IRON CURTAIN // MULTIPLAYER COLD WAR CLASSROOM GEOPOLITICS SIMULATOR
echo   Powered by Open-Historia 3D Canvas Map + Palantir C2 Strategic Defense Console
echo ===============================================================================
echo.
echo Starting C2 Classroom Server on http://localhost:3000 ...
echo LAN access enabled for students across classroom devices.
echo.
start "" http://localhost:3000
node server/server.js
pause
