from playwright.sync_api import sync_playwright

url = "https://detail.tmall.com/item.htm?id=777464567977"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(url)

    print("页面已打开")

    input("按回车关闭浏览器")

    browser.close()