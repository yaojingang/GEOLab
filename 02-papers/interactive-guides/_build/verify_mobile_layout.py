"""Regression check for long formula and chart labels on narrow screens."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CASES = [
    ("02_GEO方法优化_What_Generative_Search_Engines_Like.html", 7),
    ("04_AI搜索实证_Characterizing_Web_Search_in_Generative_AI_Age.html", 15),
    ("12_搜索架构与抓取_B01_The_Anatomy_of_a_Large_Scale_Hypertextual_Web_Search_Engine.html", 7),
    ("12_搜索架构与抓取_B05_Graph_Structure_in_the_Web.html", 12),
    ("13_链接分析与外链理论_C09_The_Intelligent_Surfer_Probabilistic_Combination_of_Link_and_Content_Information_in_PageRank.html", 7),
    ("16_机器学习排序_F01_Optimizing_Search_Engines_Using_Clickthrough_Data.html", 7),
]

failures = []
with sync_playwright() as runtime:
    browser = runtime.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 375, "height": 812}, reduced_motion="reduce")
    context.route("https://hm.baidu.com/**", lambda route: route.fulfill(status=200, body=""))
    page = context.new_page()
    for name, number in CASES:
        page.goto((ROOT / name).as_uri())
        page.wait_for_function('window.PGS && document.querySelector(".page.on")')
        for mode in ("plain", "pro"):
            page.locator(f'[data-mode="{mode}"]').click()
            page.evaluate("n => PGS.go(n - 1, false)", number)
            width = page.evaluate("document.documentElement.scrollWidth")
            if width > 376:
                failures.append({"file": name, "page": number, "mode": mode, "width": width})
    browser.close()
print(json.dumps({"cases": len(CASES), "failures": failures}, ensure_ascii=False, indent=2))
raise SystemExit(bool(failures))
