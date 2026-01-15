# 交互日志：Jekyll静态网页面包屑导航实现

**日期**: 2026年1月15日

## 用户需求

用户要求在Jekyll博客中实现静态网页的面包屑导航功能，需求如下：

1. **实现方式**: Jekyll Liquid模板 + HTML + CSS
2. **显示位置**: 文章标题上方
3. **交互风格**: 链接式（所有层级都是可点击的链接，除当前页面）
4. **项目信息**:
   - 项目使用Jekyll 3.10.0 + jekyll-theme-Cayman主题
   - 没有自定义的_layouts和_includes目录
   - 所有页面默认使用远程主题的布局

## 执行过程

### 第一阶段：方案规划

1. **分析项目结构**
   - 确认项目使用外部主题（Cayman）
   - 需要创建本地的_layouts目录来扩展主题功能
   - Jekyll会自动使用本地布局而非远程主题布局

2. **设计实现方案**
   - 创建_includes/breadcrumb.html：面包屑Liquid组件
   - 创建_layouts/default.html：主布局（包含面包屑）
   - 创建_layouts/post.html：文章布局（继承default）
   - 创建assets/css/breadcrumb.css：样式文件

### 第二阶段：核心组件开发

#### 1. 面包屑组件 (_includes/breadcrumb.html)

**关键特性**:
- 自动解析当前页面URL路径
- 使用Liquid case语句将路径映射到中文标题
- 支持任意嵌套层级
- 当前页面显示为非链接文本

**核心逻辑**:
```liquid
1. 解析page.url，分割路径为数组
2. 第一项始终是"首页"链接
3. 对于中间路径层级：
   - 使用case语句查找对应的中文标题
   - 生成链接到该层级的index.html
4. 最后一项是当前页面标题，不生成链接
```

**支持的路径映射**:
```
prevention                    → 糖尿病的预防：构建健康生活防线
prevention/diet              → 健康饮食：通过均衡营养预防糖尿病
prevention/exercise          → 规律运动：如何通过科学锻炼有效预防糖尿病
prevention/sleep             → 充足睡眠
prevention/emotion           → 情绪管理
```

#### 2. 主布局 (_layouts/default.html)

**修改内容**:
- 基于Cayman主题的原始HTML结构
- 在`<main id="content">`内容前加入面包屑组件
- 添加条件语句：仅在非首页时显示面包屑

```liquid
{% unless page.url == '/' %}
  {% include breadcrumb.html %}
{% endunless %}
```

- 在head中引入breadcrumb.css

#### 3. 文章布局 (_layouts/post.html)

**简单设计**:
```yaml
---
layout: default
---

{{ content }}
```
- 继承default布局，自动获得面包屑功能

#### 4. 样式文件 (assets/css/breadcrumb.css)

**设计原则**:
- 视觉统一：颜色与Cayman主题保持一致
- 清晰层级：使用背景色和边框区分面包屑区域
- 响应式：移动端优化，自动调整间距和字号
- 可打印：打印时隐藏面包屑导航

**关键样式**:
```css
.breadcrumb {
  背景色：#f6f8fa（浅灰）
  左边框：4px solid #157878（主题色）
  字体大小：0.9rem（略小于正文）
  圆角：6px
}

.breadcrumb-link {
  颜色：#157878（主题色）
  悬停效果：颜色加深+下划线
}

.breadcrumb-current {
  颜色：#666（灰色）
  字重：600（加粗）
}

分隔符：使用CSS ::after伪元素生成" >"
```

### 第三阶段：测试与验证

1. **编译测试**
   - 运行`bundle exec jekyll build`
   - 所有markdown文件正确编译
   - CSS文件正确输出到_site目录

2. **效果验证**
   ```
   检测点1：防止diet页面
   URL: /prevention/diet/balanced-diet-diabetes-prevention.html
   面包屑: 首页 > 糖尿病的预防... > 健康饮食... > 食疗知慧...
   ✓ 所有中文标题正确显示
   ✓ 前三项是链接，最后一项是文本
   
   检测点2：exercise页面
   URL: /prevention/exercise/how-daily-exercise-prevents-diabetes.html
   面包屑: 首页 > 糖尿病的预防... > 规律运动... > 运动是良医...
   ✓ 标题映射正确
   
   检测点3：首页
   URL: /
   面包屑: 不显示（符合预期）
   
   检测点4：prevention目录
   URL: /prevention/index.html
   面包屑: 首页 > 糖尿病的预防...
   ✓ 只显示两层
   ```

## 最终成果

### 创建的文件

| 文件位置 | 大小 | 说明 |
|---------|------|------|
| `_includes/breadcrumb.html` | 2.5KB | 面包屑Liquid组件 |
| `_layouts/default.html` | 4.0KB | 主布局文件 |
| `_layouts/post.html` | 39B | 文章布局文件 |
| `assets/css/breadcrumb.css` | 1.3KB | 样式文件 |

### 功能特性

✅ **自动生成**：无需为每篇文章手动配置
✅ **智能映射**：路径自动映射到中文标题
✅ **完全链接**：除当前页面外，所有层级都是链接
✅ **响应式**：自适应移动端和桌面端
✅ **无依赖**：纯CSS+Liquid实现，无JavaScript
✅ **SEO友好**：语义化HTML标签（nav, ol, li）
✅ **零性能开销**：静态编译，运行时无额外计算

## 使用和维护

### 扩展新路径

当添加新的目录或需要显示新的导航路径时：

1. 编辑`_includes/breadcrumb.html`
2. 在case语句中添加新的映射：
   ```liquid
   {%- when 'new/path' -%}
     {%- assign display_title = '新路径的中文标题' -%}
   ```

### 自定义样式

编辑`assets/css/breadcrumb.css`，可调整：
- 背景色和边框色
- 字体大小和粗细
- 分隔符样式
- 链接颜色和悬停效果
- 响应式断点

### 问题排查

**问题**：面包屑不显示
**解决**：检查页面的Front Matter中layout是否为default或post

**问题**：标题显示为英文（如"Prevention"）
**解决**：检查_includes/breadcrumb.html中的case语句是否包含该路径

**问题**：CSS未加载
**解决**：确保jekyll build后_site/assets/css/breadcrumb.css存在

## 技术总结

### 使用的Liquid特性
- `split`：字符串分割
- `remove_first`：移除首字符
- `replace`：字符串替换
- `capitalize`：首字母大写
- `case/when`：条件分支
- `unless`：反向条件判断
- `forloop`：循环遍历

### CSS特性
- Flexbox布局（flex-wrap用于响应式）
- CSS伪元素（::after生成分隔符）
- 媒体查询（@media用于响应式设计）
- 打印样式（@media print）

### Jekyll概念
- `_includes`：可复用的组件文件
- `_layouts`：页面布局模板
- `page.url`：当前页面的URL路径
- `page.title`：当前页面的Front Matter标题
- `site.pages`：站点所有页面的集合（本实现未使用，改用case映射）

## 后续建议

1. **配置化路径映射**：考虑在_config.yml中定义路径映射，而非硬编码在模板中
2. **动态标题读取**：如果Jekyll能正确加载site.pages，可改用动态读取
3. **国际化支持**：考虑添加语言切换，支持英文、日文等
4. **结构化数据**：添加Schema.org的BreadcrumbList标记，增强SEO
5. **快捷导航**：考虑将面包屑扩展为下拉菜单，便于快速跳转

---

**实现者**: OpenCode AI  
**完成时间**: 2026年1月15日  
**项目**: jingchunzhang.github.io 博客  
**相关链接**: https://blog.tangyou.space
