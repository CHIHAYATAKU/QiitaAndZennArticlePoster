# Qiita and Zenn Article Poster

このアプリケーションは、QiitaとZennに記事を同時に投稿するためのツールです。

## 必要な環境変数

`config.py` ファイルに以下のトークンを設定してください。

- `QIITA_API_TOKEN`
- `ZENN_API_TOKEN`

### Windowsでの設定方法

1. `config.py` ファイルを編集して、以下のようにトークンを設定します。

```python
# config.py

QIITA_API_TOKEN = "your_qiita_api_token"
ZENN_API_TOKEN = "your_zenn_api_token"
```
## 処理の流れ
1. 投稿したい記事の作成
2. qiitaは直接，ZennはGitHub連携で投稿する（仮）

## アイデア
1. githubアカウントのディレクトリにpushできるようにする．
2. 事前にgitやgithubの環境を作ってもらう必要がある
3. リポジトリ名，ディレクトリ名は指定したい．できれば各々選択できるようにしたい．
4. アプリケーションのoutディレクトリに記事を保存しておきたい．編集のために．
5. gitに保存する前にフォーマットをそれぞれで整えてcommitできるようにする．その日の日付や記事番号でよさそう．（ファイルは2つ，それぞれtxtファイルでよさそう）
6. どちらの記事もGitHub連携で投稿する（仮）
