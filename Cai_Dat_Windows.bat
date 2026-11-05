@echo off
chcp 65001 >nul
title Cài Đặt Camoufox Antidetect Pro cho Windows
echo ========================================================
echo   CÀI ĐẶT CAMOUFOX ANTIDETECT PRO CHO WINDOWS
echo ========================================================
echo.

:: Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] KHÔNG TÌM THẤY PYTHON TRÊN MÁY BẠN!
    echo.
    echo Vui lòng cài đặt Python (phiên bản 3.10 trở lên) từ https://www.python.org/downloads/
    echo QUAN TRỌNG: Hãy tích chọn "Add python.exe to PATH" khi cài đặt!
    echo.
    pause
    exit /b 1
)

echo [*] Đang khởi tạo môi trường ảo Python (.venv)...
python -m venv .venv
if %errorlevel% neq 0 (
    echo [X] Lỗi khi tạo môi trường ảo .venv!
    pause
    exit /b 1
)

echo [*] Đang nâng cấp pip...
.venv\Scripts\python.exe -m pip install --upgrade pip

echo [*] Đang cài đặt các thư viện cần thiết (camoufox, pywebview, requests...)...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [X] Lỗi khi cài đặt thư viện!
    pause
    exit /b 1
)

echo.
echo [*] Đang tải bản build trình duyệt Camoufox Windows và mô hình Fingerprint...
.venv\Scripts\camoufox.exe fetch
if %errorlevel% neq 0 (
    echo [X] Lỗi khi tải bản build Camoufox!
    pause
    exit /b 1
)

echo.
echo ========================================================
echo   [OK] CÀI ĐẶT THÀNH CÔNG HOÀN TẤT!
echo.
echo   Từ bây giờ, bạn chỉ cần nhấp đúp vào file:
echo   👉 Chay_App_Windows.bat
echo   để mở ứng dụng Desktop bất cứ lúc nào!
echo ========================================================
echo.
pause

