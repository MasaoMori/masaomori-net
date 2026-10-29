---
layout: "page"
title: "過去のイベント"
permalink: "/events/"
searchable: false
---
{% assign events = site.pages | where: 'content_type', 'tribe_events' | where: 'lang', 'ja' | sort: 'date' | reverse %}
{% include post-list.html items=events %}
