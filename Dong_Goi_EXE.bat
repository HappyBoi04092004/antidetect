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

echo [*] Đang tiến hành đóng gói (thu thập đầy đủ dữ liệu camoufox, fpgen, language_tags, playwright)...
set "TEMP_DIST=%LOCALAPPDATA%\Temp\camoufox_dist"
set "TEMP_WORK=%LOCALAPPDATA%\Temp\camoufox_build"
rd /s /q "%TEMP_DIST%" 2>nul
rd /s /q "%TEMP_WORK%" 2>nul

.venv\Scripts\pyinstaller.exe --onedir --noconsole --name "Camoufox Antidetect" --add-data "ui;ui" --icon="camoufox.ico" --collect-all camoufox --collect-all fpgen --collect-all language_tags --collect-all playwright --distpath "%TEMP_DIST%" --workpath "%TEMP_WORK%" app.py --clean -y

if %errorlevel% equ 0 (
    if not exist "dist\Camoufox Antidetect" mkdir "dist\Camoufox Antidetect"
    xcopy "%TEMP_DIST%\Camoufox Antidetect\*" "dist\Camoufox Antidetect\" /e /y /i /q
    if exist "ui" xcopy "ui" "dist\Camoufox Antidetect\ui\" /e /y /i /q
    if exist "safe_bgm" xcopy "safe_bgm" "dist\Camoufox Antidetect\safe_bgm\" /e /y /i /q
    echo.
    echo ========================================================
    echo   [OK] ĐÃ ĐÓNG GÓI THÀNH CÔNG!
    echo.
    echo   File chạy .exe nằm trong thư mục:
    echo   👉 dist\Camoufox Antidetect\Camoufox Antidetect.exe
    echo ========================================================
) else (
    echo [X] Quá trình đóng gói thất bại.
)
echo.
pause
