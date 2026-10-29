# masaomori.net — Jekyll migration review

2022-03-25 BackWPupバックアップをもとに作成したサイトです。2026-10-29にレビュー・公開承認済み。独自ドメインとDNSは切り替えていません。

GitHub Pages: https://masaomori.github.io/masaomori-net/

Repository: https://github.com/MasaoMori/masaomori-net

## 内容

- 公開記事6件（非表示設定の4件を除外）。固定ページ10件のうち1件は保護ページの案内のみ。
- Wiki 1件、過去のイベント3件。記事日時、更新日時、公開著者名、カテゴリー、元のIDを保持。
- 画像120ファイル、公開PDF1件、ZIP2件、XLSX1件。元の `/wp-content/uploads/` パスを保持。
- 日本語スラッグ、カテゴリ・日付別一覧、RSS、サイトマップ、静的検索。
- `?p=ID` / `?page_id=ID` / `?attachment_id=ID` はJavaScriptで移動。HTTP 301ではありません。
- qTranslateの日本語・英語内容を分離。英訳がないページは原文を表示。
- フォーム・会員機能・パスワード付きダウンロードは案内へ変更。
- `/ir-analysis/BSJE_bench/` と `/ir-analysis/twiuni/` はバックアップに実体がなく、案内ページのみ。
- PlantUMLショートコードはソース表示。動的な図の描画は含みません。

本文にある所属、料金、日時などはバックアップ時点の記載です。原SQL、wp-config.php、パスワード、会員情報、問い合わせ送信内容、制限付き資料は含みません。

## ローカルで生成・確認する

Ruby 3.3以降、Bundler、Python 3を用意し、このフォルダーで実行します。

```sh
bundle install
bundle exec jekyll build
python3 scripts/validate.py _site
bundle exec jekyll serve --host 127.0.0.1
```

`http://127.0.0.1:4000/` を開きます。Pythonの検証スクリプトは標準ライブラリのみを使用します。

リポジトリ名をURLの一部にする場合も検証できます。

```sh
bundle exec jekyll build --baseurl /repository-name
python3 scripts/validate.py _site /repository-name
```

## 承認後のGitHub Pages公開

1. このフォルダーの内容だけを公開先リポジトリに配置します。元ZIP・SQLや調査用作業フォルダーをアップロードしないでください。
2. リポジトリのSettings → Pages → SourceをGitHub Actionsに設定します。
3. 内容確認後に `Publish reviewed site` ワークフローを手動実行します。pushによる自動公開は設定していません。
4. GitHub側の生成・検証・公開結果と実際のURLを確認します。GitHub上の動作はまだ未検証です。
5. 独自ドメインとDNSの切り替えは、ユーザーの承認後に別途行います。現在CNAMEファイルはありません。

`_config.yml` は現在 `url: https://masaomori.github.io`、`baseurl: /masaomori-net` としています。独自ドメインへの切り替え承認後は `url: https://www.masaomori.net`、`baseurl: ""` に変更します。GitHub Pagesでのビルド・公開方法は[公式ドキュメント](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)を参照しています。

## デザイン

バックアップのHappenStance 3.0.1（Tomas Toman）とテーマ設定を調査し、青い見出し・濃いメニュー・2カラム構成を静的サイト向けに組み直しました。ヘッダーは元のアップロード写真から1枚を選択しています。元テーマのランダム切り替えやPHPの完全な再現ではありません。外部フォントやWordPressプラグインへの依存はありません。

## 検証の範囲

ローカルの生成結果、内部リンク・フラグメント、画像・配布ファイル、記事IDマップ、検索データを検証しています。外部サイト4件は取得制限などで確認できず、リンクの有効性を保証していません。分析ツールの案内ページはリンク先が存在してもツール本体の復元を意味しません。
