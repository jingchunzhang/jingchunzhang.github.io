import os
import re

# More general replacements
replacements = [
    (r"糖尿病康复", "糖尿病缓解"),
    (r"康复期", "缓解期"),
    (r"康复阶段", "缓解阶段"),
    (r"康复专题", "缓解专题"),
    (r"康复指南", "缓解指南"),
    (r"康复管理", "缓解管理"),
    (r"康复首页", "缓解首页"),
    (r"康复栏目", "缓解栏目"),
    (r"康复方法", "缓解方法"),
    (r"康复建议", "缓解建议"),
    (r"心理康复", "心理缓解"),
    (r"视觉康复", "视觉缓解"),
    (r"术后康复", "术后缓解"),
    (r"居家康复", "居家缓解"),
    (r"康复训练", "缓解期训练"),
    (r"康复锻炼", "缓解期锻炼"),
    (r"康复进展", "缓解进展"),
    (r"康复质量", "缓解质量"),
    (r"康复路径", "缓解路径"),
    (r"康复目标", "缓解目标"),
    (r"康复思路", "缓解思路"),
    (r"康复的关键", "缓解的关键"),
    (r"从预防到康复", "从预防到缓解"),
    (r"Diabetes Recovery", "Diabetes Remission"),
    (r"Diabetes recovery", "Diabetes remission"),
    (r"\bRecovery\b", "Remission"),
    (r"\brecovery\b", "remission"),
    (r"康复", "缓解"),
]

base_dir = "blog/diabetes"

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".md") or file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = content
            for old, new in replacements:
                new_content = re.sub(old, new, new_content)
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated terms in: {path}")
