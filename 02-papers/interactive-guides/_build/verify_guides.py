#!/usr/bin/env python3
"""Exercise every generated course in an isolated Chromium browser."""
from pathlib import Path
import json,re,urllib.parse,csv
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
REPORT=ROOT/'_build'/'verification.json'
files=sorted(x for x in ROOT.glob('*.html') if x.name!='index.html')
results=[];errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch()
 context=browser.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce')
 context.route('https://hm.baidu.com/**',lambda route:route.fulfill(status=200,body=''))
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 for idx,f in enumerate(files,1):
  out={'file':f.name,'bytes':f.stat().st_size};before=len(errors)
  page.set_viewport_size({'width':1440,'height':900});page.goto(f.as_uri());page.wait_for_function('window.PGS && document.querySelector(".page.on")')
  out['pages']=page.locator('.page').count();out['plain_overflow']=page.evaluate('PGS.checkAll()')
  page.locator('[data-mode="pro"]').click();out['pro_overflow']=page.evaluate('PGS.checkAll()')
  out['chapters']=page.locator('.toc-ch').count()
  out['missing_notes']=page.locator('.page').evaluate_all('(ps)=>ps.flatMap((p,i)=>!p.querySelector(".notes")?.textContent.trim()?[i+1]:[])')
  # Each course's ten-plus learning activities, including non-default states.
  interaction=[]
  if page.locator('.lesson').count():
   for pi in range(out['pages']):
    page.evaluate('(i)=>PGS.go(i)',pi)
    actions=page.locator('.page.on [data-action]').evaluate_all('(bs)=>bs.filter(b=>!b.disabled&&!b.dataset.action.toLowerCase().includes("quiz")&&!b.dataset.action.includes("copy")&&b.dataset.action!=="answer").map(b=>[b.dataset.action,b.dataset.value||null])')
    for a,v in actions:
     q='.page.on [data-action="'+a+'"]'+('[data-value="'+v+'"]' if v is not None else '')
     if page.locator(q).count() and not page.locator(q).first.is_disabled():page.locator(q).first.evaluate('(b)=>b.click()')
    bad=page.evaluate('(i)=>{const b=document.querySelectorAll(".b-body")[i];return b.scrollHeight>b.clientHeight+2||b.scrollWidth>b.clientWidth+2}',pi)
    if bad:interaction.append(pi+1)
   # Five-question flow, check feedback and result rendering.
   page.evaluate('PGS.go(22)')
   for q in range(5):
    page.locator('.page.on [data-action="answer"]').first.click();page.locator('.page.on [data-action="nextQuiz"]').click()
   out['quiz_complete']=page.locator('.page.on').inner_text().find('自测完成')>=0
  out['interaction_overflow']=interaction
  page.set_viewport_size({'width':375,'height':812})
  out['mobile_overflow']=page.evaluate('''()=>{const bad=[];for(let i=0;i<document.querySelectorAll('.page').length;i++){PGS.go(i,false);if(document.documentElement.scrollWidth>innerWidth+1)bad.push([i+1,document.documentElement.scrollWidth]);}return bad}''')
  page.locator('[data-mode="plain"]').click()
  out['mobile_plain_overflow']=page.evaluate('''()=>{const bad=[];for(let i=0;i<document.querySelectorAll('.page').length;i++){PGS.go(i,false);if(document.documentElement.scrollWidth>innerWidth+1)bad.push([i+1,document.documentElement.scrollWidth]);}return bad}''')
  out['errors']=errors[before:]
  # Resolve every local hyperlink; fragments and original-source links need no filesystem lookup.
  from bs4 import BeautifulSoup
  soup=BeautifulSoup(f.read_text(),'html.parser');broken=[]
  for a in soup.find_all('a',href=True):
   h=urllib.parse.urlsplit(a['href'])
   if not h.scheme and h.path and not (f.parent/urllib.parse.unquote(h.path)).exists():broken.append(a['href'])
  out['broken_links']=broken;results.append(out)
  if idx%10==0:print(f'checked {idx}/{len(files)}',flush=True)
 # Homepage filters, search, paths and mobile.
 page.goto((ROOT/'index.html').as_uri());page.wait_for_selector('.paper');home={'initial_count':page.locator('.paper').count()}
 page.locator('#search').fill('SCAR');home['search_count']=page.locator('.paper').count();page.locator('#clear').click()
 for button in page.locator('#paths button').all():button.click()
 home['path_links']=page.locator('.path-stops a').count();page.locator('#categories [data-category="06_风险操纵"]').click();home['risk_count']=page.locator('.paper').count();page.locator('#clear').click()
 home['mobile_width']=page.evaluate('document.documentElement.scrollWidth');home['viewport_width']=375
 page.evaluate('scrollTo(0,0)');page.screenshot(path=str(ROOT/'_build/home-mobile.png'),full_page=False)
 page.set_viewport_size({'width':1440,'height':900});page.evaluate('scrollTo(0,0)');page.screenshot(path=str(ROOT/'_build/home-desktop.png'),full_page=False)
 for name,pi in [('02_GEO方法优化_IF_GEO_Conflict_Aware_Instruction_Fusion.html',4),('03_GEO测量评估_From_Citation_Selection_to_Citation_Absorption.html',11),('06_风险操纵_SafeGEO_Recommendation_Agents.html',12)]:
  fp=ROOT/name
  if fp.exists():
   page.goto(fp.as_uri());page.evaluate('(i)=>PGS.go(i)',pi);page.screenshot(path=str(ROOT/'_build'/('preview-'+name+'.png')))
 browser.close()
report={'courses':len(files),'pages':sum(x['pages'] for x in results),'courses_detail':results,'homepage':home,'browser_errors':errors}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2))
fail=[x for x in results if any(x.get(k) for k in ['plain_overflow','pro_overflow','interaction_overflow','mobile_overflow','mobile_plain_overflow','errors','broken_links']) or not x.get('quiz_complete',True) or x['missing_notes'] or x['chapters']!=7 or x['pages']!=23 or x['bytes']>200*1024]
print(json.dumps({'courses':len(files),'pages':report['pages'],'failed_courses':len(fail),'failures':fail,'homepage':home},ensure_ascii=False,indent=2))
raise SystemExit(bool(fail or len(files)!=121 or home['initial_count']!=122 or home['mobile_width']>375))
