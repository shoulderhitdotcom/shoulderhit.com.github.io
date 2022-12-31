---
layout: default
title: shoulderhit.com - your source of pro go/baduk/weiqi happenings is live!
---

Welcome to shoulderhit.com where we will bring you the latest and greatest in the world of professional Go/Baduk/Weiqi


<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
      {{ post.excerpt }}
    </li>
  {% endfor %}
</ul>
