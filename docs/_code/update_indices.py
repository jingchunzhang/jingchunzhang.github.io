import os

titles = {
    "basics": ("糖尿病基础", "Diabetes Basics"),
    "prevention": ("糖尿病预防", "Diabetes Prevention"),
    "treatment": ("糖尿病治疗", "Diabetes Treatment"),
    "rehabilitation": ("糖尿病缓解", "Diabetes Remission"),
    "monitoring": ("糖尿病监测", "Diabetes Monitoring"),
    "complications": ("糖尿病并发症", "Diabetes Complications"),
    "diet": ("糖尿病饮食", "Diabetes Diet"),
    "caregiver": ("护理人员指南", "Caregiver Guide"),
    "research": ("糖尿病研究", "Diabetes Research"),
    "topics": ("糖尿病专题", "Diabetes Topics"),
    "prevention/sleep": ("糖尿病预防 - 睡眠", "Diabetes Prevention - Sleep"),
    "prevention/exercise": ("糖尿病预防 - 运动", "Diabetes Prevention - Exercise"),
    "prevention/emotion": ("糖尿病预防 - 情绪", "Diabetes Prevention - Emotion"),
    "prevention/diet": ("糖尿病预防 - 饮食", "Diabetes Prevention - Diet"),
    "rehabilitation/sleep": ("糖尿病缓解 - 睡眠", "Diabetes Remission - Sleep"),
    "rehabilitation/diet": ("糖尿病缓解 - 饮食", "Diabetes Remission - Diet"),
    "rehabilitation/exercise": ("糖尿病缓解 - 运动", "Diabetes Remission - Exercise"),
    "rehabilitation/emotion": ("糖尿病缓解 - 情绪", "Diabetes Remission - Emotion"),
    "treatment/sleep": ("糖尿病治疗 - 睡眠", "Diabetes Treatment - Sleep"),
    "treatment/diet": ("糖尿病治疗 - 饮食", "Diabetes Treatment - Diet"),
    "treatment/emotion": ("糖尿病治疗 - 情绪", "Diabetes Treatment - Emotion"),
    "treatment/exercise": ("糖尿病治疗 - 运动", "Diabetes Treatment - Exercise"),
}

base_dir = "blog/diabetes"

updated_dirs = []

for root, dirs, files in os.walk(base_dir):
    if root == base_dir:
        continue
    
    rel_path = os.path.relpath(root, base_dir)
    
    # Check if it's a category directory (in titles) or already has an index file
    has_index = "index.md" in files or "index-en.md" in files
    if rel_path not in titles and not has_index:
        continue

    # Skip date-based directories like research/2026-03
    if any(part.startswith("202") and len(part) == 7 and part[4] == "-" for part in rel_path.split(os.sep)):
        continue
    
    if rel_path in titles:
        title_zh, title_en = titles[rel_path]
    else:
        # Fallback for existing index files not in titles mapping
        name = os.path.basename(root).replace("-", " ").capitalize()
        title_zh, title_en = (f"糖尿病 - {name}", f"Diabetes - {name}")

    path_in_include = f"/{root}/"
    if not path_in_include.endswith("/"):
        path_in_include += "/"

    # Update index.md
    index_md_path = os.path.join(root, "index.md")
    content_zh = f"""---
layout: default
title: {title_zh}
lang: zh
---
# {title_zh}专题
{{% include post-list.html path='{path_in_include}' %}}
---
[返回糖尿病中心](../)
"""
    with open(index_md_path, "w", encoding="utf-8") as f:
        f.write(content_zh)
    
    # Update index-en.md
    index_en_md_path = os.path.join(root, "index-en.md")
    content_en = f"""---
layout: default
title: {title_en}
lang: en
---
# {title_en} Articles
{{% include post-list.html path='{path_in_include}' %}}
---
[Back to Diabetes Hub](../)
"""
    with open(index_en_md_path, "w", encoding="utf-8") as f:
        f.write(content_en)
    
    updated_dirs.append(rel_path)

print("Updated directories:")
for d in sorted(updated_dirs):
    print(f"- {d}")
