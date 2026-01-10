---
layout: default
title: "运动与糖尿病预防"
---

## 运动与糖尿病预防

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
      <a href="{{ site.baseurl }}/prevention/exercise/how-daily-exercise-prevents-diabetes.md">运动是良医：如何通过科学锻炼有效预防糖尿病</a>
      <span> - 2026-01-10</span>
  </li>
</ul>
