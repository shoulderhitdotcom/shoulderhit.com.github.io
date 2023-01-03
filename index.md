---
layout: default
title: shoulderhit.com - your source of pro go/baduk/weiqi happenings is live!
---

Welcome to shoulderhit.com where we will bring you the latest and greatest in the world of professional Go/Baduk/Weiqi



{% for post in site.posts %}
<div>
<h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
<blockquote>
{{ post.excerpt | markdownify }}
</blockquote>
</div>
{% endfor %}