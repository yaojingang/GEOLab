#!/usr/bin/env python3
"""Verify a single PGS course file. Usage: verify_one.py <file.html> [--shots DIR]"""
import sys, json, urllib.parse
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
name = sys.argv[1]
shots = None
if '--shots' in sys.argv:
    shots = Path(sys.argv[sys.argv.index('--shots')+1]); shots.mkdir(parents=True, exist_ok=True)
f = ROOT/name
if not f.exists():
    print(json.dumps({'error': f'file not found: {name}'})); sys.exit(2)
out = {'file': name, 'bytes': f.stat().st_size}
errors = []
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce')
    page = context.new_page(); page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(f.as_uri()); page.wait_for_function('window.PGS && document.querySelector(".page.on")')
    out['pages'] = page.locator('.page').count()
    out['chapters'] = page.locator('.toc-ch').count()
    out['plain_overflow'] = page.evaluate('PGS.checkAll()')
    if shots:
        for i in range(out['pages']):
            page.evaluate('(i)=>PGS.go(i)', i)
            page.wait_for_timeout(60)
            page.screenshot(path=str(shots/f'p{i+1:02d}.png'))
    page.locator('[data-mode="pro"]').click(); out['pro_overflow'] = page.evaluate('PGS.checkAll()')
    if shots:
        for i in [0, 6, 10, 14]:
            page.evaluate('(i)=>PGS.go(i)', i); page.wait_for_timeout(60)
            page.screenshot(path=str(shots/f'pro{i+1:02d}.png'))
        page.locator('[data-mode="plain"]').click()
    out['missing_notes'] = page.locator('.page').evaluate_all('(ps)=>ps.flatMap((p,i)=>!p.querySelector(".notes")?.textContent.trim()?[i+1]:[])')
    interaction = []
    if page.locator('.lesson').count():
        for pi in range(out['pages']):
            page.evaluate('(i)=>PGS.go(i)', pi)
            actions = page.locator('.page.on [data-action]').evaluate_all('(bs)=>bs.filter(b=>!b.disabled&&!b.dataset.action.toLowerCase().includes("quiz")&&!b.dataset.action.includes("copy")&&b.dataset.action!=="answer").map(b=>[b.dataset.action,b.dataset.value||null])')
            for a, v in actions:
                q = '.page.on [data-action="'+a+'"]'+('[data-value="'+v+'"]' if v is not None else '')
                if page.locator(q).count() and not page.locator(q).first.is_disabled(): page.locator(q).first.evaluate('(b)=>b.click()')
            bad = page.evaluate('(i)=>{const b=document.querySelectorAll(".b-body")[i];return b.scrollHeight>b.clientHeight+2||b.scrollWidth>b.clientWidth+2}', pi)
            if bad: interaction.append(pi+1)
        page.evaluate('PGS.go(22)')
        quiz_ok = True
        for q in range(5):
            ans = page.locator('.page.on [data-action="answer"]')
            if not ans.count(): quiz_ok = False; break
            ans.first.click()
            nxt = page.locator('.page.on [data-action="nextQuiz"]')
            if not nxt.count(): quiz_ok = False; break
            nxt.click()
        out['quiz_complete'] = quiz_ok and page.locator('.page.on').inner_text().find('自测完成') >= 0
    out['interaction_overflow'] = interaction
    page.set_viewport_size({'width': 375, 'height': 812})
    out['mobile_overflow'] = page.evaluate('''()=>{const bad=[];for(let i=0;i<document.querySelectorAll('.page').length;i++){PGS.go(i,false);if(document.documentElement.scrollWidth>innerWidth+1)bad.push([i+1,document.documentElement.scrollWidth]);}return bad}''')
    page.locator('[data-mode="plain"]').click()
    out['mobile_plain_overflow'] = page.evaluate('''()=>{const bad=[];for(let i=0;i<document.querySelectorAll('.page').length;i++){PGS.go(i,false);if(document.documentElement.scrollWidth>innerWidth+1)bad.push([i+1,document.documentElement.scrollWidth]);}return bad}''')
    out['errors'] = errors
    soup = BeautifulSoup(f.read_text(), 'html.parser'); broken = []
    for a in soup.find_all('a', href=True):
        h = urllib.parse.urlsplit(a['href'])
        if not h.scheme and h.path and not (f.parent/urllib.parse.unquote(h.path)).exists(): broken.append(a['href'])
    out['broken_links'] = broken
    browser.close()
checks = ['plain_overflow','pro_overflow','interaction_overflow','mobile_overflow','mobile_plain_overflow','missing_notes','errors','broken_links']
out['pass'] = (not any(out.get(k) for k in checks)) and out.get('quiz_complete', True) and out['pages'] == 23 and out['chapters'] == 7 and out['bytes'] < 200*1024
print(json.dumps(out, ensure_ascii=False, indent=1))
sys.exit(0 if out['pass'] else 1)
