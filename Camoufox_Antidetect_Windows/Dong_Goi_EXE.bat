@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Đóng gói file .EXE cho Windows
echo ========================================================
echo   ĐÓNG GÓI CAMOUFOX ANTIDETECT THÀNH FILE .EXE (WINDOWS)
echo ========================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [X] Vui lòng chạy Cai_Dat_Windows.bat trước khi đóng gói!
    pause
    exit /b 1
)

echo [*] Đang cài đặt PyInstaller...
.venv\Scripts\pip.exe install pyinstaller

echo [*] Đang tiến hành đóng gói...
.venv\Scripts\pyinstaller.exe --noconsole --name "Camoufox Antidetect" --add-data "ui;ui" --icon="camoufox.ico" app.py

echo.
echo ========================================================
echo   [OK] ĐÃ ĐÓNG GÓI THÀNH CÔNG!
echo.
echo   File chạy .exe nằm trong thư mục:
echo   👉 dist\Camoufox Antidetect\Camoufox Antidetect.exe
echo ========================================================
echo.
pause

