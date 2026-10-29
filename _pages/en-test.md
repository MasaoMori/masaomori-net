---
layout: "page"
title: "TEST"
date: "2020-04-09 17:04:19 +0900"
last_modified_at: "2020-04-09 17:16:51 +0900"
permalink: "/en/test/"
wp_id: 377
author: "masa"
excerpt: ""
lang: "en"
categories: []
english_url: "/en/test/"
japanese_url: "/test/"
restricted: false
has_translation: false
content_type: "page"
searchable: false
---
> English translation is unavailable. The original Japanese text follows.
{: .archive-notice role="note" }

<details class="diagram-source" open markdown="1">

<summary>図のソース（PlantUML）</summary>

```text
title
相談シートフロー(正課)
出願前の相談
end title

actor "出願学生" as stu
actor "受け入れ教員" as teach
actor "国際連携課" as icd
actor "アドバイザー" as adv
actor "部局担当課" as sec
actor "学務部各関係課" as ssd

stu <-> teach : 受入事前調整
activate teach
rnote over teach : シート記入
teach -> icd : シート提出
activate icd
opt 記入事項問題アリ
icd -> teach : 差し戻し
teach -> icd : 再提出
else 記入事項問題ナシ
deactivate teach
icd -> adv : 審査依頼
deactivate icd
activate adv
end

rnote over adv : 記載内容および法令確認
opt 審査の必要アリ
adv -> teach : 詳細確認
activate teach
rnote over teach : 資料訂正
teach -> adv : 再提出
deactivate teach
rnote over adv : 確認
loop 問題アリ
adv -> teach : 再確認&修正依頼
activate teach
rnote over teach : 指導内容等改訂
teach -> adv : 再提出
deactivate teach
else 問題ナシ
end
else 審査不要(または完了)
rnote over adv : 結論
adv -> teach : 審査結果(注意事項等)
deactivate teach
end

adv -> icd : 情報共有
deactivate adv
teach -> stu : 受け入れ承諾通知
icd-> sec : 情報共有
icd -> ssd : 情報共有
[<- stu : 出願へ
```

</details>
