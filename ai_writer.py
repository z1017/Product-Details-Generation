import requests
import re

API_KEY = "你的 API Key"

def auto_detect_brand(title):
    # 自动识别标题开头的品牌名（中文或英文）
    match = re.match(r"^([A-Za-z\u4e00-\u9fa5]+)", title)
    if match:
        return match.group(1)
    return ""

def clean_brand(text, brand):
    if brand:
        text = text.replace(brand, "")
    return text

def generate_content(product):
    # 自动识别品牌
    brand = auto_detect_brand(product["title"])

    # 清洗品牌
    title = clean_brand(product["title"], brand)
    desc = clean_brand(product["description"], brand)

    prompt = f"""
You are a professional e-commerce copywriter specializing in Shopify and independent website product pages.

Remove any brand names that may appear in the product info.

Generate the following content in BOTH Chinese and English.
Do NOT include:
- Any brand names
- Any store names
- Any sales data or reviews
- Any marketing claims
- Any markdown syntax (no **, no -, no #)
- No emojis

Content needed:
1. A short Chinese product title (no brand names).
2. A short English product title (no brand names).
3. A full Chinese product description that combines selling points and detailed features into one clean text (multiple paragraphs allowed, no markdown).
4. A full English product description with the same structure.

Product Info:
{title}
{desc}

Return EXACTLY in this format:

ChineseTitle:
EnglishTitle:
ChineseDescription:
EnglishDescription:
"""

    r = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages":[{"role":"user","content":prompt}],
            "temperature":0.6
        }
    )

    text = r.json()["choices"][0]["message"]["content"]

    def extract(label):
        pattern = rf"{label}:(.*?)(?=\n[A-Za-z]+Title:|\nChinese|English|$)"
        match = re.search(pattern, text, re.S)
        return match.group(1).strip() if match else ""

    return {
        "title_cn": extract("ChineseTitle"),
        "title_en": extract("EnglishTitle"),
        "desc_cn": extract("ChineseDescription"),
        "desc_en": extract("EnglishDescription"),
    }
