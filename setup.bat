@echo off
chcp 65001 > nul
echo.
echo  ================================================
echo   影片 Demo 生成器  ^|  一鍵安裝
echo  ================================================
echo.

echo  [1/2] 安裝 yt-dlp（影片下載工具）...
pip install -q yt-dlp
if %errorlevel% neq 0 (
    echo  X yt-dlp 安裝失敗，請先確認 Python 已安裝
    echo    下載：https://www.python.org/downloads/
    pause & exit /b 1
)
echo  OK yt-dlp 已安裝

echo.
echo  [2/2] 安裝 FFmpeg（影片剪輯工具）...
where ffmpeg >nul 2>&1
if %errorlevel% equ 0 (
    echo  OK FFmpeg 已存在，略過
) else (
    winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
    if %errorlevel% neq 0 (
        echo  X FFmpeg 安裝失敗
        echo    請手動安裝：https://ffmpeg.org/download.html
        echo    安裝後將 ffmpeg.exe 加入 PATH
        pause & exit /b 1
    )
    echo  OK FFmpeg 已安裝
)

echo.
echo  ================================================
echo   安裝完成！
echo.
echo   使用方式：
echo     1. 在這個資料夾放入 index.html（H5 頁面）
echo     2. 執行  python serve.py
echo     3. 瀏覽器自動開啟，填寫工單後產出腳本
echo     4. 將工單 .md 丟給 Claude Code 生成影片
echo     5. 影片生成完後 H5 右下角自動顯示
echo  ================================================
echo.
pause
