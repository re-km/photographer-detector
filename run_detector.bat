@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

REM 必要なライブラリのチェックとインストール
python -c "import mediapipe" >nul 2>&1
if !errorlevel! neq 0 (
    echo [INFO] 必要なライブラリ (mediapipe) が見つかりません。インストールします...
    pip install mediapipe opencv-python
    if !errorlevel! neq 0 (
        echo [ERROR] ライブラリのインストールに失敗しました。
        echo Pythonまたはpipがインストールされているか確認してください。
        pause
        exit /b
    )
)

REM 入力フォルダ（カレントディレクトリ）と出力フォルダの設定
set INPUT_DIR=.
set OUTPUT_DIR=detected_images

if not exist "%OUTPUT_DIR%" (
    mkdir "%OUTPUT_DIR%"
)

echo 画像抽出を開始します...
echo 入力: カレントディレクトリ
echo 出力: %OUTPUT_DIR%

python detect_photographer.py "%INPUT_DIR%" "%OUTPUT_DIR%"

echo.
echo 処理が完了しました。
pause
