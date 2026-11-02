@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Camoufox Antidetect Pro

if not exist ".venv\Scripts\python.exe" (
    echo [!] Chưa tìm thấy môi trường cài đặt.
    echo Đang tự động chạy file cài đặt Cai_Dat_Windows.bat...
    call Cai_Dat_Windows.bat
)

:: Khởi chạy ứng dụng không hiện cửa sổ cmd đen
start "" ".venv\Scripts\pythonw.exe" app.py
if %errorlevel% neq 0 (
    ".venv\Scripts\python.exe" app.py
)

