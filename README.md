# 画像抽出ツール (Image Extraction Tool)

フォルダ内の画像から、顔や手が写っている写真（撮影者の写り込みなど）を検出し、別のフォルダに**移動**するツールです。

## 必要要件

- Python 3.7以上
- 必要なライブラリ (以下のコマンドでインストールできます)

```bash
pip install -r requirements.txt
```

## 使い方

### バッチファイルでの実行 (Windows)

画像が入っているフォルダに `run_detector.bat` と `detect_photographer.py` を置き、`run_detector.bat` をダブルクリックしてください。
そのフォルダ内の画像をスキャンし、検出された画像を `detected_images` フォルダに**移動**します。

**注意**: 元の画像は入力フォルダから削除されます。

※ 初回実行時に必要なライブラリがない場合は、自動的にインストールされます。

### 例

`photos` フォルダ内の画像を処理したい場合:
1. `photos` フォルダの中に `run_detector.bat` と `detect_photographer.py` をコピーします。
2. `run_detector.bat` を実行します。
3. 顔や手が写っている画像が `photos/detected_images` に移動します。

## 仕組み

GoogleのMediaPipeライブラリを使用して、画像内の「顔」と「手」を検出します。どちらか一方でも検出された場合、その画像は出力フォルダに**移動**されます。
