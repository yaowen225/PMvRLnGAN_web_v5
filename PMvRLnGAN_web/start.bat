@echo off
echo 正在啟動 PMvRLnGAN Web 應用...
echo.

REM 檢查Python是否已安裝
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 錯誤: 未找到Python。請確保Python已安裝並添加到PATH中。
    pause
    exit /b 1
)

REM 檢查是否已安裝所需的依賴項
echo 檢查依賴項...
pip install -r requirements.txt

REM 啟動應用程序
echo 啟動應用程序...
python run.py

pause 