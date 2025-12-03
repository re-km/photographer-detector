@echo off
setlocal

REM 入力フォルダと出力フォルダの設定
set INPUT_DIR=input_images
set OUTPUT_DIR=detected_images

REM フォルダが存在しない場合は作成（入力フォルダはユーザーが用意する必要があるため警告）
if not exist "%INPUT_DIR%" (
    echo [ERROR] 入力フォルダ "%INPUT_DIR%" が見つかりません。
    echo フォルダを作成し、画像を配置してください。
    pause
    exit /b
)

if not exist "%OUTPUT_DIR%" (
    mkdir "%OUTPUT_DIR%"
)

echo 画像抽出を開始します...
echo 入力: %INPUT_DIR%
echo 出力: %OUTPUT_DIR%

python detect_photographer.py "%INPUT_DIR%" "%OUTPUT_DIR%"

echo.
echo 処理が完了しました。
pause
