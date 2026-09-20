@echo off
title The Iron Curtain - Cold War Geopolitics Simulator
echo ===================================================
echo   THE IRON CURTAIN: MULTIPLAYER CLASSROOM SIMULATOR
echo ===================================================
echo.
echo Launching local server bound to 0.0.0.0:8501...
echo Students can connect from any LAN device via http://^<host-ip^>:8501
echo.
.venv\Scripts\streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
pause
