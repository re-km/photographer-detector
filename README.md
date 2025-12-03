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

付属の `run_detector.bat` をダブルクリックするだけで実行できます。
初回実行時は `input_images` フォルダがない場合エラーになりますが、フォルダを作成して画像を入れれば動作します。

### 例

`input_images` フォルダ内の画像をスキャンし、検出された画像を `detected_images` フォルダにコピーする場合:

```bash
python detect_photographer.py input_images detected_images
```

## 仕組み

GoogleのMediaPipeライブラリを使用して、画像内の「顔」と「手」を検出します。どちらか一方でも検出された場合、その画像は出力フォルダにコピーされます。
