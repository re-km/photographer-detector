# 画像抽出ツール (Image Extraction Tool)

フォルダ内の画像から、顔や手が写っている写真（撮影者の写り込みなど）を検出し、別のフォルダにコピーするツールです。

## 必要要件

- Python 3.7以上
- 必要なライブラリ (以下のコマンドでインストールできます)

```bash
pip install -r requirements.txt
```

## 使い方

以下のコマンドを実行してください。

```bash
python detect_photographer.py [入力フォルダ] [出力フォルダ]
```

### オプション

- `--threshold`: 検出の信頼度しきい値（デフォルト: 0.5）。値を上げると誤検出が減りますが、検出漏れが増える可能性があります。

### バッチファイルでの実行 (Windows)

画像が入っているフォルダに `run_detector.bat` と `detect_photographer.py` を置き、`run_detector.bat` をダブルクリックしてください。
そのフォルダ内の画像をスキャンし、検出された画像を `detected_images` フォルダにコピーします。

※ 初回実行時に必要なライブラリがない場合は、自動的にインストールされます。

### 例

`photos` フォルダ内の画像を処理したい場合:
1. `photos` フォルダの中に `run_detector.bat` と `detect_photographer.py` をコピーします。
2. `run_detector.bat` を実行します。

```bash
python detect_photographer.py input_images detected_images
```

## 仕組み

GoogleのMediaPipeライブラリを使用して、画像内の「顔」と「手」を検出します。どちらか一方でも検出された場合、その画像は出力フォルダにコピーされます。
