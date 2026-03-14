from playwright.sync_api import sync_playwright, TimeoutError

def scrape_product(url, state_file="taobao_state.json"):
    data = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            storage_state=state_file,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            java_script_enabled=True,
        )
        page = context.new_page()

        print("正在打开页面:", url)
        try:
            page.goto(url, timeout=60000)
        except TimeoutError:
            print("⚠️ 页面打开超时")
            browser.close()
            return None

        print("当前 URL:", page.url)
        print("页面标题:", page.title())

        # 登录/风控检测
        if "login" in page.url or "sec.taobao.com" in page.url:
            print("⚠️ 当前未登录或触发风控，无法抓取商品页")
            browser.close()
            return None

        # 直接用 tab 标题作为商品标题
        raw_title = page.title()
        title = raw_title.replace("-tmall.com天猫", "").strip()
        print("最终标题:", title)

        # 价格（尽量抓）
        try:
            price = page.locator(".tm-price, [class*=price]").first.inner_text().strip()
        except:
            price = ""

        # 卖点区域
        try:
            props = page.locator(".tm-propertylist, .tb-property").inner_text().strip()
        except:
            props = ""

        # 图文详情（常在 iframe）
        detail = ""
        try:
            for frame in page.frames:
                try:
                    body_text = frame.locator("body").inner_text().strip()
                    if len(body_text) > 100:
                        detail = body_text
                        break
                except:
                    pass
        except:
            pass

        browser.close()

    if not title:
        print("⚠️ 标题为空，抓取失败")
        return None

    description = (props + "\n" + detail)[:1500]

    data["title"] = title
    data["price"] = price
    data["description"] = description

    return data


if __name__ == "__main__":
    test_url = "https://detail.tmall.com/item.htm?id=777464567977"
    result = scrape_product(test_url)
    print(result)
