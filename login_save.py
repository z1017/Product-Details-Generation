from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://login.tmall.com")  # 淘宝/天猫登录页

    print("请在浏览器中完成登录，登录完成后按 Enter 继续...")
    input()

    # 保存登录状态
    context.storage_state(path="tmall_auth.json")
    print("登录状态已保存")
    browser.close()