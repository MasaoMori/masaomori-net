# masaomori.net — Jekyll migration review

2022-03-25 BackWPupバックアップをもとに作成したサイトです。2026-10-29にレビュー・公開承認済み。公開ドメインは `masaomori.net` です。

公開サイト: https://masaomori.net/

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


## Markdownで本文を管理する

記事・固定ページ・一覧・転送ページのソースは `.md` です。公開時にはJekyllがHTMLを生成します。共通レイアウトやフォームなどの部品は `_layouts/`・`_includes/` のHTMLにまとめ、RSS・サイトマップはHTML/XMLテンプレートを使用しています。

### よく編集するファイル

| 内容 | ファイル |
| --- | --- |
| プロフィール | `_pages/cv.md` |
| 問い合わせ案内 | `_pages/contact-me.md` |
| ツール案内 | `_pages/tools.md` |
| 教材の配布ページ | `_pages/大学irカリキュラム教材.md` |
| 学生成績サンプル | `_pages/irtext-data-sample.md` |
| 過去の記事 | `_posts/YYYY-MM-DD-記事名.md` |
| 英語ページ | `_pages/en-ページ名.md` |

先頭の `---` で囲まれた設定では、既存ページの `permalink` を維持すると元のURLを保てます。`wp_id`、`restricted` は移行時点の状態を示す記録です。`restricted` を指定しても静的サイトの本文にパスワードは掛かりません。旧保護ページの本文はこのリポジトリに含みません。

### 本文の書き方

````markdown
## 見出し

通常の段落です。**太字**も使えます。

- 箇条書き
- 箇条書き

[プロフィール]({{ '/cv/' | relative_url }})

![画像の説明]({{ '/wp-content/uploads/2017/03/71PSFYFVKtL-212x300.jpg' | relative_url }})

```text
コードや図のソース
```
````

画像サイズなどを残す必要がある場合は、画像の後ろに `{: width="212" height="300" }` を付けられます。折りたたみ表示の `<details>` など、Markdownだけでは表せない部品は一部HTMLを併用します。

### 新しい記事を追加する

`_posts/2026-10-29-my-new-post.md` のような名前でファイルを作ります。先頭の日付は記事の日付に合わせます。

```markdown
---
title: "新しい記事のタイトル"
date: "2026-10-29 09:00:00 +0900"
permalink: /my-new-post/
author: "森 雅生"
categories: ["告知"]
---

ここから本文を書きます。
```

記事の標準レイアウト・日本語・検索対象の設定は `_config.yml` に定義しています。記事一覧、既存のカテゴリ・日付別一覧、RSS、サイト内検索のデータは再公開時に本文から自動生成されるため、HTMLや `assets/search.json` を手作業で更新する必要はありません。新しいカテゴリーをサイドバーにも出したい場合は `_data/categories.json` に追加します。新しい年月日の専用一覧URLが必要な場合は `_pages/date-*.md` を参考に一覧ページを追加します。

新しい固定ページは `_pages/ページ名.md` に作り、先頭に `layout: page`、`title`、`permalink`、`lang: ja`、`searchable: true` を指定します。英語ページは別ファイルなので、日本語本文の変更後は対応する英語ページも必要に応じて編集してください。

### GitHubで編集して公開する

1. `_posts/` または `_pages/` の `.md` を編集してコミットします。
2. Actions → **Publish reviewed site** → **Run workflow** を実行します。
3. 生成・検証・公開が成功したら、サイト上の表示を確認します。

push時の自動公開は設定していません。`_data/content.json` は移行時点の記録で、日常の本文編集先ではありません。

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

## GitHub Pagesでの公開・更新

1. このフォルダーの内容だけを公開先リポジトリに配置します。元ZIP・SQLや調査用作業フォルダーをアップロードしないでください。
2. リポジトリのSettings → Pages → SourceをGitHub Actionsに設定します。
3. 内容確認後に `Publish reviewed site` ワークフローを手動実行します。pushによる自動公開は設定していません。
4. GitHub側の生成・検証・公開結果と実際のURLを確認します。2026-10-29にGitHub側の生成・検証・公開が成功し、公開URLで記事・画像・検索・旧記事IDリンクの動作も確認しました。

   公開ワークフローの記録: https://github.com/MasaoMori/masaomori-net/actions/runs/40819073018
5. 独自ドメインとDNSの切り替えは、ユーザーの承認後に別途行います。現在CNAMEファイルはありません。

`_config.yml` はGitHub Pagesの独自ドメイン設定に合わせて `url: https://masaomori.net`、`baseurl: ""` としています。GitHub Pagesでのビルド・公開方法は[公式ドキュメント](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)を参照しています。

## デザイン

バックアップのHappenStance 3.0.1（Tomas Toman）とテーマ設定を調査し、青い見出し・濃いメニュー・2カラム構成を静的サイト向けに組み直しました。ヘッダーは元のアップロード写真から1枚を選択しています。元テーマのランダム切り替えやPHPの完全な再現ではありません。外部フォントやWordPressプラグインへの依存はありません。

## 検証の範囲

ローカルの生成結果、内部リンク・フラグメント、画像・配布ファイル、記事IDマップ、検索データを検証しています。外部サイト4件は取得制限などで確認できず、リンクの有効性を保証していません。分析ツールの案内ページはリンク先が存在してもツール本体の復元を意味しません。
