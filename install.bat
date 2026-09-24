@echo off
echo Installing GameZone Agent dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo ==============================================
echo Dependencies installed successfully!
echo You can now configure config.py and run start_agent.vbs
echo ==============================================
pause
