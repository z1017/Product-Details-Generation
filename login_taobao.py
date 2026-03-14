from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    context = browser.new_context()

    page = context.new_page()

    page.goto("https://login.taobao.com")

    print("请在浏览器中登录淘宝")

    input("登录完成后按回车")

    context.storage_state(path="taobao_state.json")

    print("登录状态已保存")

    browser.close()