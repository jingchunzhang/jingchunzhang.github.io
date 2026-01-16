---
layout: default
title: "Exercise and Diabetes Prevention"
lang: en
translation_key: prevention/exercise/index
---

## Exercise and Diabetes Prevention

<ul>
  {% for post in site.posts %}
    {% if post.url contains '/prevention/exercise/' %}
      <li>
        <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a>
        <span> - {{ post.date | date: "%Y-%m-%d" }}</span>
      </li>
    {% endif %}
  {% endfor %}
  <li>
      <a href="{{ site.baseurl }}/prevention/exercise/how-daily-exercise-prevents-diabetes-en.md">Exercise as Medicine: How Scientific Training Effectively Prevents Diabetes</a>
      <span> - 2026-01-10</span>
  </li>
</ul>

[Back to Prevention Home](../index-en.md)
