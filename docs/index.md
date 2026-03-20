---
layout: default
title: Tangyou Space｜糖友空间
lang: zh
translation_key: home
---

# Tangyou Space｜糖友空间

> **[About Us / 关于我们](/about/)** | **[English Version](./index-en)**

我们致力于构建糖尿病全周期管理的内容生态与数字服务。

---

## 👨‍👩‍👧‍👦 面向个人 (For Individuals)

我们的核心内容覆盖糖尿病管理的三个关键阶段：

<div class="features-grid">
  <div class="feature-card">
    <h3>🛡️ 预防阶段 (Prevention)</h3>
    <p>早期筛查、饮食干预与生活方式调整，降低发病风险。</p>
    <a href="./blog/prevention/" class="btn">浏览预防指南 &rarr;</a>
  </div>
  <div class="feature-card">
    <h3>💊 治疗阶段 (Treatment)</h3>
    <p>科学用药、饮食处方与运动疗法，实现平稳控糖。</p>
    <a href="./blog/treatment/" class="btn">浏览治疗方案 &rarr;</a>
  </div>
  <div class="feature-card">
    <h3>🌱 康复阶段 (Rehabilitation)</h3>
    <p>并发症管理、长期健康维护与逆转可能探索。</p>
    <a href="./blog/rehabilitation/" class="btn">浏览康复策略 &rarr;</a>
  </div>
</div>

---

## 🏢 面向企业 (For Business)

我们为健康科技企业与开发者提供专业服务：

*   **[独立站应用开发](/products/)**：Shopify / WordPress 插件定制
*   **[广告联盟技术](/solutions/)**：追踪、归因与结算系统搭建
*   **[SEO 增长咨询](/seo/)**：垂直领域的流量获取与转化优化

---

## 📰 最新文章 (Latest from Blog)

{% include post-list.html limit=3 show_tags=false %}

<p style="text-align: center; margin-top: 2rem;">
  <a href="./blog/" class="btn btn-outline">浏览全部文章 (View All) &rarr;</a>
</p>

<style>
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}
.feature-card {
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #f9f9f9;
  text-align: center;
}
.feature-card h3 {
  margin-top: 0;
  color: #159957;
}
.feature-card .btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #159957;
  color: white;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.9em;
}
.feature-card .btn:hover {
  background: #1e7e34;
}
.btn-outline {
  border: 2px solid #159957;
  color: #159957;
  background: transparent;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
}
.btn-outline:hover {
  background: #159957;
  color: white;
}
</style>
