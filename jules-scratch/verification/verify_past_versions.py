from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    versions_to_capture = [
        "version-2015",
        "version-2016",
        "version-2020"
    ]

    for version_name in versions_to_capture:
        page.goto(f"http://localhost:8000/{version_name}/index.html")
        screenshot_path = f"jules-scratch/verification/screenshot_{version_name}.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot taken for {version_name}")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
