import pandas as pd
from scraper import scrape_product
from ai_writer import generate_content

INPUT_FILE = "products.xlsx"
OUTPUT_FILE = "products_output.xlsx"

def main():
    df = pd.read_excel(INPUT_FILE)

    cols = [
        "AI中文标题", 
        "AI英文标题",
        "AI中文详情",
        "AI英文详情"
    ]

    for c in cols:
        if c not in df.columns:
            df[c] = ""

    for idx, row in df.iterrows():
        url = str(row["链接"]).strip()
        if not url or url == "nan":
            continue

        print(f"\n===== 处理第 {idx} 行 =====")
        print("链接:", url)

        product = scrape_product(url)
        if product is None:
            continue

        ai = generate_content(product)

        df.at[idx, "AI中文标题"] = ai["title_cn"]
        df.at[idx, "AI英文标题"] = ai["title_en"]
        df.at[idx, "AI中文详情"] = ai["desc_cn"]
        df.at[idx, "AI英文详情"] = ai["desc_en"]

        df.to_excel(OUTPUT_FILE, index=False)

    print("\n✅ 全部处理完成，已写入:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
