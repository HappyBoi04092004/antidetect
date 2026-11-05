@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Camoufox Antidetect Pro

if not exist ".venv\Scripts\python.exe" (
    echo [!] Chua tim thay moi truong cai dat .venv.
    echo Dang tu dong chay file cai dat Cai_Dat_Windows.bat...
    call Cai_Dat_Windows.bat
)

echo [*] Dang khoi dong Camoufox Antidetect Studio...
".venv\Scripts\python.exe" app.py
if %errorlevel% neq 0 (
    echo.
    echo [LOI] Co loi xay ra khi chay ung dung. Nhan phim bat ky de thoat...
    pause >nul
)
