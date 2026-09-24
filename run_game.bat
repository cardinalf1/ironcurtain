@echo off
title The Iron Curtain - Cold War Geopolitics Simulator
echo ===============================================================================
echo   THE IRON CURTAIN // MULTIPLAYER COLD WAR CLASSROOM GEOPOLITICS SIMULATOR
echo   Palantir C2 Strategic Defense Console (1945-1991 • 10 Eras)
echo ===============================================================================
echo.
echo Launching C2 Operations Console on http://localhost:8501 ...
echo Accessible across classroom devices via your local IP address.
echo.
start "" http://localhost:8501
.venv\Scripts\streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
pause
