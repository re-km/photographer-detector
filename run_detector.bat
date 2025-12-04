@echo off
chcp 65001 >nul
setlocal

echo 起動中...

REM Pythonの確認
python --version >nul 2>&1
if %errorlevel% neq 0 goto NoPython

REM ライブラリの確認
python -c "import mediapipe" >nul 2>&1
if %errorlevel% neq 0 goto InstallLib

goto Run

:InstallLib
echo [INFO] 必要なライブラリ (mediapipe) が見つかりません。インストールします...
pip install mediapipe opencv-python
if %errorlevel% neq 0 goto InstallFail
goto Run

:NoPython
echo [ERROR] Pythonが見つかりません。
echo Pythonをインストールし、PATHに通してください。
pause
exit /b

:InstallFail
echo [ERROR] ライブラリのインストールに失敗しました。
pause
exit /b

:Run
REM ==========================================
REM 設定項目 (必要に応じて変更してください)
REM ==========================================

REM 顔検出の閾値 (0.0 〜 1.0)
REM 値を上げると判定が厳しくなり、下げると緩くなります。
set FACE_THRESHOLD=0.5

REM 手検出の閾値 (0.0 〜 1.0)
set HAND_THRESHOLD=0.5

REM 顔検出モデル (0: 至近距離, 1: 全距離)
REM 通常は 1 でOKです。
set MODEL_SELECTION=1

REM デバッグモード (ON: 1, OFF: 0)
REM ONにすると、検出結果を描画した画像を保存します。
set DEBUG_MODE=0

REM ==========================================

set INPUT_DIR=.
set OUTPUT_DIR=detected_images

if not exist "%OUTPUT_DIR%" (
    mkdir "%OUTPUT_DIR%"
)

echo 画像抽出を開始します...
echo 入力: カレントディレクトリ
echo 出力: %OUTPUT_DIR%
echo 設定: Face=%FACE_THRESHOLD%, Hand=%HAND_THRESHOLD%, Model=%MODEL_SELECTION%, Debug=%DEBUG_MODE%

REM デバッグオプションの構築
set DEBUG_OPT=
if "%DEBUG_MODE%"=="1" (
    set DEBUG_OPT=--debug
)

python detect_photographer.py "%INPUT_DIR%" "%OUTPUT_DIR%" --face_threshold %FACE_THRESHOLD% --hand_threshold %HAND_THRESHOLD% --model_selection %MODEL_SELECTION% %DEBUG_OPT%

echo.
echo 処理が完了しました。
pause
