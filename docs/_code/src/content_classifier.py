import requests
import json
import config

STAGES = ["prevention", "treatment", "rehabilitation"]
ASPECTS = ["diet", "exercise", "sleep", "emotion"]

CLASSIFICATION_PROMPT = """分析以下糖尿病相关内容的分类。

内容标题：{title}
内容摘要：{content}

请根据以下标准分类：

**阶段 (stage)**：
- prevention（预防）：适合糖尿病高危人群、未确诊但想预防的人
- treatment（治疗）：适合已确诊糖尿病患者，正在治疗中
- rehabilitation（康复）：适合血糖已稳定，进入康复/维持阶段

**方面 (aspect)**：
- diet（饮食）：涉及食物、食谱、营养、餐单等
- exercise（运动）：涉及运动、锻炼、体力活动等
- sleep（睡眠）：涉及睡眠、作息、休息等
- emotion（情绪）：涉及压力、情绪、心理、心情等

请返回JSON格式：
{{"stage": "prevention/treatment/rehabilitation", "aspect": "diet/exercise/sleep/emotion"}}
"""

def classify_content(title: str, content: str) -> dict:
    if config.USE_VOLCENGINE_LLM:
        return _classify_volcengine(title, content)
    else:
        return _classify_rule_based(title, content)

def _classify_volcengine(title: str, content: str) -> dict:
    content_sample = content[:500] if len(content) > 500 else content
    prompt = CLASSIFICATION_PROMPT.format(title=title, content=content_sample)
    
    url = f"{config.VOLCENGINE_LLM_API_BASE}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.VOLCENGINE_LLM_API_KEY}"
    }
    data = {
        "model": config.VOLCENGINE_LLM_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()
        text = result['choices'][0]['message']['content']
        
        json_start = text.find('{')
        json_end = text.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            json_str = text[json_start:json_end]
            return json.loads(json_str)
    except Exception as e:
        print(f"Classification error: {e}")
    
    return _classify_rule_based(title, content)

def _classify_rule_based(title: str, content: str) -> dict:
    text = (title + " " + content).lower()
    
    stage = "prevention"
    if any(w in text for w in ["治疗", "diagnosed", "diagnosis", "medication", "insulin", "药物", "医生", "patient", "患病", "确诊"]):
        stage = "treatment"
    elif any(w in text for w in ["康复", "recovered", "稳定", "维持", "maintenance", "康复期"]):
        stage = "rehabilitation"
    
    aspect = "diet"
    if any(w in text for w in ["运动", "exercise", "跑步", "步行", "锻炼", "walk", "run", "workout", "健身"]):
        aspect = "exercise"
    elif any(w in text for w in ["睡眠", "sleep", "休息", "熬夜", "作息", "夜", "bed", "卧室", "bath", "shower", "淋浴", "洗澡"]):
        aspect = "sleep"
    elif any(w in text for w in ["情绪", "emotion", "压力", "stress", "心情", "焦虑", "抑郁", "心理", "mental"]):
        aspect = "emotion"
    
    return {"stage": stage, "aspect": aspect}

def get_subdir(stage: str, aspect: str) -> str:
    return f"{stage}/{aspect}"

def get_all_categories():
    categories = []
    for stage in STAGES:
        for aspect in ASPECTS:
            categories.append({
                "stage": stage,
                "aspect": aspect,
                "subdir": f"{stage}/{aspect}",
                "name": f"{stage}_{aspect}"
            })
    return categories
