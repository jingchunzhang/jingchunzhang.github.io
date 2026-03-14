import random
from typing import Dict, List
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import config

# Prompt 变异池 - 体裁变体
GENRE_VARIANTS = {
    "对比清单": """请生成一篇"{keyword}"的对比清单文章。
要求：
1. 列出 3-5 个关键对比点
2. 每个对比点用表格或列表清晰展示
3. 给出明确的优缺点总结
4. 适合糖尿病患者或高危人群阅读""",
    
    "step_by_step": """请生成一篇"{keyword}"的 Step-by-step 教程。
要求：
1. 使用清晰的步骤编号
2. 每个步骤包含具体操作说明
3. 添加"小贴士"或"注意事项"
4. 语言通俗易懂，适合新手""",
    
    "avoidance_guide": """请生成一篇"{keyword}"的避坑指南。
要求：
1. 列出常见的 5-8 个误区或错误做法
2. 解释为什么这些是错的
3. 提供正确的做法或替代方案
4. 语气友善，像朋友提醒""",
    
    "buying_guide": """请生成一篇"{keyword}"的选购指南。
要求：
1. 明确目标人群和使用场景
2. 列出选购要点（功能、价格、品牌等）
3. 给出推荐产品或方案
4. 包含购买链接或建议（联盟营销导向）""",
    
    "experience_share": """请生成一篇"{keyword}"的经验分享文章。
要求：
1. 第一人称叙述，有真实感
2. 分享具体的使用体验或经历
3. 包含成功经验和踩坑经历
4. 情感真挚，避免过于机械"""
}

# Prompt 变异池 - 视角变体
PERSONA_VARIANTS = {
    "budget_conscious": """你是一位注重性价比的实用主义者，擅长在预算有限的情况下找到最好的解决方案。
写作风格：务实、直接、注重实际效果，不追求高价但也不贪便宜。""",
    
    "senior_patient": """你是一位有着 10 年糖尿病管理经验的资深糖友，亲身尝试过各种方法。
写作风格：温暖、耐心、经验丰富，分享的经历让人感到可信和安心。""",
    
    "medical_researcher": """你是一位关注最新医学研究的健康编辑，擅长解读科研论文。
写作风格：严谨、数据导向、注重证据，但会用通俗语言解释。""",
    
    "nutritionist": """你是一位专业营养师，专注糖尿病饮食管理。
写作风格：专业、细致、注重科学依据，给出具体的饮食建议。"""
}

# YMYL 领域安全指令
YMYL_SAFETY_PROMPT = """
【安全约束 - 必须遵守】
1. 禁止生成任何具体的用药剂量建议
2. 禁止生成停药或改变治疗方案的建议
3. 禁止推荐未经验证的保健品或治疗方法
4. 文章开头必须包含免责声明："{disclaimer}"
5. 聚焦于生活方式调整（饮食、运动、监测），而非医疗建议
""".format(disclaimer=config.YMYL_DISCLAIMER)

# 双语支持 - 语言变体
LANGUAGE_VARIANTS = {
    "zh": """请用简体中文写作""",
    "en": """Please write in English"""
}

# 图片生成提示词
IMAGE_PROMPT_TEMPLATE = """为文章"{keyword}"生成一个描述性图片提示词，用于AI图片生成。
要求：
1. 描述一个与主题相关的医学/健康场景
2. 包含具体的人物、环境、动作描述
3. 使用英文描述
4. 50-100个词
5. 输出格式：只需输出图片提示词，不要其他内容"""

def build_prompt(keyword: str, genre: str = None, persona: str = None, lang: str = "zh") -> str:
    if genre is None:
        genre = random.choice(list(GENRE_VARIANTS.keys()))
    if persona is None:
        persona = random.choice(list(PERSONA_VARIANTS.keys()))
    
    genre_template = GENRE_VARIANTS.get(genre, GENRE_VARIANTS["step_by_step"])
    persona_instructions = PERSONA_VARIANTS.get(persona, PERSONA_VARIANTS["senior_patient"])
    lang_instruction = LANGUAGE_VARIANTS.get(lang, LANGUAGE_VARIANTS["zh"])
    
    prompt = f"""{persona_instructions}

{lang_instruction}

{genre_template}

{config.YMYL_DISCLAIMER}

请生成一篇高质量的文章，围绕关键词：{keyword}

文章要求：
- 字数 800-1500 字
- 结构清晰，有明确的小标题
- 适合 SEO，包含关键词的自然分布
- 在文章开头或适当位置添加1-2张相关图片（使用 Markdown 图片语法，描述性 alt 文本）
- 结尾可以引导下载相关电子书
"""
    return prompt

def build_image_prompt(keyword: str) -> str:
    return IMAGE_PROMPT_TEMPLATE.format(keyword=keyword)

def get_random_variant() -> tuple:
    genre = random.choice(list(GENRE_VARIANTS.keys()))
    persona = random.choice(list(PERSONA_VARIANTS.keys()))
    return genre, persona

def get_all_genres() -> List[str]:
    return list(GENRE_VARIANTS.keys())

def get_all_personas() -> List[str]:
    return list(PERSONA_VARIANTS.keys())
