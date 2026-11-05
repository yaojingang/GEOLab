#!/usr/bin/env python3
"""Build offline PGS courses from curated notes and local paper evidence."""
from pathlib import Path
import csv, html, json, re, subprocess, tempfile, hashlib
from analytics import with_baidu_analytics

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
ROOT = OUT.parent
SAMPLE = OUT/'01_GEO基础框架_GEO_Generative_Engine_Optimization.html'
WORK = Path(tempfile.gettempdir())/'geo-paper-guides'
WORK.mkdir(exist_ok=True)
E = html.escape
J = lambda x: json.dumps(x,ensure_ascii=False).replace('</','<\\/')
rows = list(csv.DictReader((ROOT/'00_资料说明/论文清单.csv').open(encoding='utf-8-sig')))
notes = {}
for line in (HERE/'course-notes.txt').read_text().splitlines():
    p=line.split('|')
    assert len(p)==13,(p[0],len(p))
    names=['id','zh','kind','question','claim','steps','findings','metrics','setting','boundary','query','before','after']
    n=dict(zip(names,p)); n["id"]=int(n["id"]); notes[n["id"]]=n
details={int(p[0]):p[1:] for p in (x.split('|') for x in (HERE/'finding-details.txt').read_text().splitlines())}
authors=json.loads((HERE/'authors.json').read_text())
actual_titles={5:'CC-GSEO-Bench: A Content-Centric Benchmark for Measuring Source Influence in Generative Search Engines',10:'What Generative Search Engines Like and How to Optimize Web Content Cooperatively',16:'From Citation Selection to Citation Absorption: A Measurement Framework for Generative Engine Optimization Across AI Search Platforms',18:'SAGEO Arena: A Realistic Environment for Evaluating Search-Augmented Generative Engine Optimization',23:'How Generative AI Disrupts Search: An Empirical Study of Google Search, Gemini, and AI Overviews',28:'Smart Search Optimization: A Theoretical Framework Integrating SEO, AEO and GEO in the Era of Genetic AI'}
numbers=json.loads((HERE/'numbers.json').read_text())
restricted={59:'PersonaGen',61:'Beyond_the_Vacuum',66:'Without',67:'With_the',70:'MAGEO'}
# Papers 71-122 live in the local-reading folder of 2026-11-04; full-text-pending rows only appear in navigation.
reading={i:q['本地阅读路径'] for i,q in enumerate(csv.DictReader((ROOT/'本地阅读_2026-11-04/122篇本地阅读清单.csv').open(encoding='utf-8-sig')),1)}
PENDING={i for i,v in reading.items() if not v}
PENDING_ZH={103:'SEO方法提升可见性'}
newpapers=json.loads((HERE/'new-papers.json').read_text()) if (HERE/'new-papers.json').exists() else {}

def paper_path(i,r):
    if r['文件名']:return ROOT/r['分类']/r['文件名']
    rel=reading.get(i,'')
    if not rel:return next(x for x in (ROOT/'本地阅读_2026-10-25').glob('*.pdf') if restricted[i] in x.name)
    return ROOT/rel[2:] if rel.startswith('./') else ROOT/rel
related={2:62,3:55,4:55,5:16,6:18,7:13,8:7,9:19,10:65,11:13,12:66,13:61,14:67,15:69,16:55,17:3,18:13,19:55,20:62,21:14,22:16,23:21,24:54,25:32,26:62,27:62,28:27,29:26,30:23,31:63,32:25,33:37,34:40,35:63,36:32,37:33,38:39,39:68,40:68,41:43,42:63,43:63,44:41,45:25,46:47,47:48,48:20,49:46,50:52,51:52,52:51,53:54,54:53,55:18,56:14,57:7,58:64,59:55,60:65,61:13,62:18,63:68,64:58,65:70,66:67,67:66,68:63,69:15,70:65}
related.update({int(k):v['related'] for k,v in newpapers.items() if v.get('related')})
# Short labels, definitions and method details are pedagogical paraphrases.
extra={
 7:'多阶段融合需要更多调用；最低收益与平均值必须同时看。',
 47:'pass@k反映多线程候选池的上限；部署时单个答案的准确率需要单列。',
 51:'节省上下文伴随召回下降；论文总结报告相对静态窗口约 3.9 个百分点的代价。',
 49:'结果不再变化与找到正确证据属于不同口径；混合比例需分层解释。',
 56:'全部复利数值来自理论模型示例，尚无真人多轮部署验证。',
 58:'契约测试只证明形式逻辑一致，语义判断质量与部署收益仍待测量。',
 59:'没有真实消费者日志对照或逐个画像的专家质量评价；合成比例不代表人口分布。',
 66:'作者披露初版查询泄露与失败置信标记，并修正评估；评分与检测能力要分开。',
 69:'英日商品推荐结果来自模拟；真实销售、注意概率与混杂变量仍需采集。'}
extra.update({int(k):v['extra'] for k,v in newpapers.items() if v.get('extra')})

def flat(s): return re.sub(r'\s+',' ',s).strip()
def excerpt(raw, pattern, limit=670, last=False):
    pat=re.compile(pattern,re.I|re.M)
    matches=list(pat.finditer(raw))
    if not matches:return None
    m=matches[-1] if last else matches[0]
    start=m.end(); page=raw[:start].count('\f')+1
    return {'text':flat(raw[start:start+limit]),'page':page}

def source_data(i,r):
    p=paper_path(i,r)
    paths={}
    if p.suffix.lower()=='.html':
        # Hilltop is stored as a saved web page; extract readable text instead of pdftotext.
        from bs4 import BeautifulSoup
        text=BeautifulSoup(p.read_text(errors='ignore'),'html.parser').get_text('\n')
        for mode in ('raw','layout'):
            target=WORK/f'{i:02d}-{mode}.txt';target.write_text(text);paths[mode]=target
    else:
        for mode,opts in [('raw',[]),('layout',['-layout'])]:
            target=WORK/f'{i:02d}-{mode}.txt'
            ok=True
            try:
                subprocess.run(['pdftotext',*opts,str(p),str(target)],check=True,stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                ok=False
            # Scanned PDFs: fall back to the OCR text cached in _build/paper-text/.
            side=HERE/'paper-text'/f'{i}-{mode}.txt'
            if (not ok and side.exists()) or (target.exists() and target.stat().st_size<200 and side.exists()):
                target.write_text(side.read_text())
            elif not target.exists():
                target.write_text('')
            paths[mode]=target
    raw=paths['raw'].read_text()
    layout=paths['layout'].read_text()
    normalized=re.sub(r'(?i)A\s+B\s+S\s+T\s+R\s+A\s+C\s+T','Abstract',raw)
    abstract=excerpt(normalized,r'^\s*Abstract(?:[.\s—-]|$)',1400)
    if i==22:abstract=excerpt(normalized,r'Abstract\s*\n\s*Abstract',1600)
    starts={38:'Major search engine providers',49:'Streaming Retrieval-Augmented Generation',50:'Retrieval-augmented generation (RAG) systems depend',52:'Retrieval-augmented generation (RAG) systems must'}
    if i in starts:
        start=raw.find(starts[i])
        if start>=0:abstract={'text':flat(raw[start:start+1900]),'page':raw[:start].count('\f')+1}
    if i==45:abstract={'text':flat(raw[raw.find('Generative search engines (GEs)'):raw.find('Key words')]),'page':1}
    if not abstract:abstract={'text':flat(raw[:1250]),'page':1}
    evidence=[{'label':'摘要与研究目标',**abstract}]
    for label,pat in [('方法与评估',r'^\s*(?:\d[\d.]*\s*)?(?:Experimental Setup|Experimental Settings|Experimental Design|Experiments|Methodology|Our Approach|Framework|Method)\s*$'),('讨论与研究边界',r'^\s*(?:\d[\d.]*\s*)?(?:Conclusion[s]?|Conclusion and Future Work|Discussion and Conclusion[s]?|Limitations)\s*$')]:
        v=excerpt(normalized,pat,1000)
        if v:evidence.append({'label':label,**v})
    # Source paragraphs are kept as evidence, never executed or followed as instructions.
    if len(evidence)<3:
        chunks=abstract['text'];evidence.append({'label':'摘要后半与证据边界','text':chunks[len(chunks)//2:],'page':abstract['page']})
    evidence=evidence[:3]
    # Preserve a real table block in the professional evidence view, when available.
    tm=re.search(r'(?m)^\s*(?:Table|TABLE)\s+(?:1|I)[:.\s]',layout)
    table=None
    if tm:
        start=tm.start(); table={'text':layout[start:start+1900].strip(),'page':layout[:start].count('\f')+1,'label':'Table 1 / Table I 原文抽取'}
    version=re.search(r'arXiv\s*:\s*(\d{4}\.\d{4,5}v\d+)',raw)
    return {'evidence':evidence,'table':table,'version':version.group(1) if version else r['来源'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_path':p}

def filename(i,r):
    if r['文件名']:return Path(r['文件名']).with_suffix('.html').name
    return paper_path(i,r).with_suffix('.html').name

sample=SAMPLE.read_text()
core_css=sample[sample.index('/* ===== PGS core v2.0'):sample.index('/* ===== PGS core end ===== */')+len('/* ===== PGS core end ===== */')]
core_js=sample[sample.index('/* ===== PGS core runtime v2.0'):sample.index('/* ===== PAPER CONTENT runtime')]
startup=sample[sample.index('/* ===== 启动 ===== */'):sample.index('</script>')]
shell=sample[sample.index('<body class='):sample.index('<!-- ============ PAPER CONTENT ·')].replace('<a class="btn" href="index.html">学习首页</a>','')
# The sample's optional music is specific to that course.
shell=re.sub(r'<div class="study-music".*?</div>', '', shell, flags=re.S)
footer=sample[sample.index('<!-- ============ PAPER CONTENT 结束'):sample.index('<div class="scrim"')]
style=(HERE/'course.css').read_text()
runtime=(HERE/'course.js').read_text()
chapters=[{'t':x,'d':y} for x,y in [('导入','明确问题与结论'),('原理','理解研究对象'),('测量','核对指标与设计'),('方法','拆解操作与对照'),('发现','逐条审视证据'),('应用','把结论转为行动'),('复盘','明确边界并检验理解')]]
syllabus=[]
all_data=[]
for i,r in enumerate(rows,1):
    if i in PENDING:continue # Full text not yet available: title-only navigation entry, no course.
    n=notes[i].copy();n['findings']=n['findings'].split('；');n['steps']=n['steps'].split('；')
    n['finding_details']=details.get(i,n['findings'])
    n['metrics']=[{'name':x.split('：',1)[0],'plain':x.split('：',1)[1]} for x in n['metrics'].split('；')]
    n['catalog_title']=r['论文题名'];n['title']=actual_titles.get(i,r['论文题名']);n['authors']=authors[str(i)];n['year']=r['年份'];n['category']=r['分类'];n['url']=r['URL'];n['file']=filename(i,r)
    n['pdf']='../'+r['分类']+'/'+r['文件名'] if r['文件名'] else ''
    n['kind_note']='概念与推导，暂无生产效果估计' if n['kind'] in ['综述','理论框架'] else '基于受测环境，迁移效果需要另测'
    n['extra']=extra.get(i,'保持论文的任务、来源范围和评估口径，再检验新场景。')
    s=source_data(i,r);n.update({k:v for k,v in s.items() if k!='source_path'})
    n['stats']=[{'v':v,'name':name,'source':src,'context':context,'page':n['evidence'][0]['page']} for v,name,src,context in numbers.get(str(i),[])]
    raw=(WORK/f'{i:02d}-raw.txt').read_text()
    for stat in n['stats']:
        if 'Conclusion' in stat['source']:
            hits=list(re.finditer(r'(?im)^\s*(?:\d[\d.]*\s*)?Conclusions?\s*$',raw))
            if hits:stat['page']=raw[:hits[0].end()].count('\f')+1
        elif stat['source'].startswith('Introduction'):
            stat['page']=2 if i==44 else 1
    other=related.get(i,62);rr=rows[other-1];n['related']={'id':other,'zh':notes[other]['zh'],'title':actual_titles.get(other,rr['论文题名']),'url':'./'+filename(other,rr),'pdf':'../'+rr['分类']+'/'+rr['文件名'] if rr['文件名'] else rr['URL'],'claim':notes[other]['claim']}
    n['strength']='弱' if n['kind'] in ['综述','理论框架'] or i in [15,56,58,59,67,69] else '中'
    n['strength_why']='本课保守评级：概念、模拟、有限样本或未完成独立语义验证。' if n['strength']=='弱' else '本课保守评级：有实证比较；样本独立性、自动评价或生产迁移仍有约束。'
    n['limitations']=[['高','研究结论有明确范围',n['boundary']],['高','评价口径决定可以推断的结果',n['extra']],['中','环境变化需要重新验证','引擎版本、界面、查询与候选来源变化时，重新执行同口径测量。该项为本课迁移审查。'],['中','证据与建议需逐项区分','应用页的行动与成熟形态是教学推断。核查原论文方法、结果及局限后再作为实验假设。'],['中','相关研究提供新的对照',n['related']['claim']],['低','原文版本与内部一致性','采用本地PDF可识别版本；不将清单页数与PDF分页混用。未逐表重算的指标仍需人工复核。']]
    # Correct two easy-to-misread numerical trade-offs without hiding them in notes.
    if i==51:n['findings'][3]='块量节省伴随召回损失'
    if i==47:n['findings'][3]='候选池上限需与单答案准确率分开'
    if i==12:n['extra']='GEO-16指质量支柱框架；摘要实际收集三个搜索平台，题名与范围应分别核对。'
    if i==28:n['extra']='原文标题使用 Genetic AI，清单采用 Generative AI；本课保留原文题名，并按摘要的生成式搜索含义解读。'
    n['quiz']=[
      {'q':'哪项最准确概括本篇的核心贡献？','o':[n['claim'],'保证所有引擎采用同一套来源','用页面总分直接替代业务结果','只需观察一次回答即可定论'],'a':0,'e':'论文的核心结论有具体对象与条件。','p':1},
      {'q':'哪条是本篇值得特别记住的发现？','o':['所有场景必然得到同等收益','只记录正向结果即可',n['findings'][2],'省略研究对象也不影响判断'],'a':2,'e':n['findings'][2]+'。','p':15},
      {'q':'本课第一个指标主要回答什么问题？','o':['网页颜色是否好看',n['metrics'][0]['plain'],'作者是否知名','页面访问量能否永远增长'],'a':1,'e':n['metrics'][0]['name']+'：'+n['metrics'][0]['plain']+'。','p':7},
      {'q':'把本篇用于新项目时，哪种做法合适？','o':['将示意值当作真实收益','跳过基线只看修改后','把理论推导当作生产实测','保留任务口径、设置对照并检查迁移边界'],'a':3,'e':n['boundary']+'。','p':17},
      {'q':'哪一项准确体现本篇的研究边界？','o':[n['boundary'],'没有任何适用范围限制','可以由引用直接推算收入','后续平台改版无需复测'],'a':0,'e':'边界决定结果可以支持哪些决策。','p':21}]
    n['quiz']=[{**q,'o':(q['o'][((i+k)%4):]+q['o'][:((i+k)%4)]),'a':(q['a']-((i+k)%4))%4} for k,q in enumerate(n['quiz'])]
    # Brief is a build input audit artifact in a temporary working directory.
    (WORK/f'{i:02d}-brief.json').write_text(J(n))
    all_data.append(n)
    if i==1:continue # Preserve the authored reference course.
    st=[(1,'课程封面',n['zh'],'cover'),(1,'学习路线','沿着问题与证据完成这门课','route'),(1,'问题场景',n['question'].replace('？',''),'scene'),(2,'核心概念','研究对象需要先拆开再比较','concept'),(2,'系统流程','方法沿着这些环节产生作用','pipeline'),(2,'研究位置','明确干预环节才能解释效果','boundary'),(3,'指标口径','指标分别回答不同的效果问题','metric'),(3,'实验设计','实验设置限定结论的适用范围','design'),(3,'对照检查','保持对照一致才能解释变化','control'),(4,'方法拆解','方法的每一步都有独立作用','method'),(4,'改动实验室','比较改动前后可以看清操作','lab'),(4,'证据读数','数字需要连同口径一起读取','numbers')]
    st += [(5,'发现'+str(k+1),f,'finding'+str(k)) for k,f in enumerate(n['findings'])]
    st += [(5,'研究对照','相关研究帮助检验迁移边界','compare'),(6,'案例拆解','把方法还原为一次具体操作','case'),(6,'角色行动','不同角色需要不同的执行清单','persona'),(6,'成熟形态','成熟工作形态可以承接研究方法','mature'),(7,'批判阅读','结论的边界决定应用的尺度','limits'),(7,'要点卡片','带走结论时也要带走条件','quotes'),(7,'课程自测','完成自测再回看薄弱环节','quiz')]
    pagehtml=[]
    for pi,(ch,short,title,typ) in enumerate(st,1):
        key=n['findings'][int(typ[-1])] if typ.startswith('finding') else {'cover':n['claim'],'numbers':'每项数值保留原论文单位、样本和适用条件。','case':'本页区分原论文案例与教学示意，不估造收益。','persona':'行动建议为本课推断，需用对照试验确认。','limits':n['boundary']}.get(typ,{'route':'先读结论，再拆原理、指标、方法、发现和应用。','scene':n['after'],'concept':n['metrics'][0]['name']+'：'+n['metrics'][0]['plain'],'pipeline':' → '.join(n['steps']),'boundary':n['boundary'],'metric':n['metrics'][0]['plain'],'design':n['setting'],'control':n['extra'],'method':n['findings'][1],'lab':n['after'],'compare':'对齐阶段与指标，才能比较不同研究。','mature':'成熟形态与研究方法的映射为本课推断。','quotes':'保留结论依据与适用条件，再转为实践动作。','quiz':'利用反馈回看对应页面，核对指标与边界。'}.get(typ,n['claim']))
        notes_text=f'这一页围绕“{title}”展开。请先观察默认状态，再操作控件并解释变化。最后核对出处，保留条件：{n["boundary"]}。'
        pagehtml.append(f'<section class="page" data-ch="{ch}" data-t="{E(short)}" data-view="{typ}"><div class="board"><div class="b-head"><h2 class="b-title">{E(title)}</h2></div><div class="b-body full"><div class="lesson" id="lesson{pi}"></div></div><div class="b-key">{E(key)}<span class="src">{E(n["evidence"][0]["label"])} · PDF p.{n["evidence"][0]["page"]}</span></div></div><div class="notes">{E(notes_text)}</div></section>')
        syllabus.append([i,n['file'],pi,ch,short,title,typ,n['evidence'][0]['label'],n['evidence'][0]['page']])
    nshell=shell.replace('论文互动课堂 · 01 GEO 基础框架','论文互动课堂 · '+E(n['category'].replace('_',' '))).replace('GEO：生成式引擎优化',E(n['zh'])).replace('Generative Engine Optimization · KDD 2024',E(n['year']+' · '+n['kind'])).replace('<a class="btn" href="../index.html">论文导航</a>','<a class="btn" href="index.html">学习首页</a><a class="btn" href="../index.html">论文导航</a>')
    drawer=f'''<div class="scrim" id="scrim"></div><aside class="drawer" id="drawer" aria-label="术语与引用"><div class="drawer-head"><b>术语与引用</b><button class="icon-btn" type="button" id="drawerClose">关闭 Esc</button></div><div class="drawer-body"><dl class="gl" id="gl"></dl><h4>文献与版本</h4><p>{E(n['title'])}</p><p>{E(n['year'])} · {E(n['version'])}</p><p><a href="{E(n['url'])}" target="_blank" rel="noopener">原文与作者署名</a></p><pre class="bib" id="bib">{E('@misc{paper'+str(i)+',\n  author = {'+n['authors'].replace('; ', ' and ')+'},\n  title = {'+n['title']+'},\n  year = {'+n['year'].split('/')[-1]+'},\n  url = {'+n['url']+'}\n}')}</pre><p class="cap">本课程为 GEO Citation Lab 原创解读，CC BY 4.0。论文版权归原作者；作者信息按本地PDF署名及元数据核对；正式引用时请再核对会议信息。教学建议及示意为本课编写。</p><p class="cap">PDF SHA-256：{n['sha256']}</p></div></aside><div class="toast" id="toast" role="status"></div>'''
    doc='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'+f'<title>{E(n["zh"])} · 论文课堂</title><meta name="description" content="{E(n["claim"])}"><meta name="paper-guide-spec" content="PGS v2.0"><meta name="paper-guide-source" content="{E(n["version"])}"><style>'+core_css+'\n'+style+'</style></head>'+nshell+'\n'.join(pagehtml)+footer+drawer+'<script>\nconst CHAPTERS='+J(chapters)+';\nconst PAPER='+J(n)+';\nconst GLOSSARY=Object.fromEntries(PAPER.metrics.map((m,i)=>["metric"+i,{t:m.name,d:m.plain}]));\nObject.assign(GLOSSARY,{geo:{t:"GEO",d:"改善来源在生成式答案中的可见性及归功的研究与实践。"},rag:{t:"RAG",d:"先检索外部资料，再以资料支持模型生成。"},baseline:{t:"基线",d:"作为效果比较起点的未修改或已有方案。"},causal:{t:"因果效应",d:"在明确干预与可比条件下，改变因素引起的结果差异。"},ablation:{t:"消融",d:"去除某个组件，比较它对整体结果的贡献。"},transfer:{t:"迁移",d:"在不同模型、数据或时期中复验方法。"}});\n'+core_js+'\n'+runtime+'\n'+startup+'</script></body></html>'
    assert len(doc.encode())<200*1024,(i,len(doc.encode()))
    # Optimized courses are guarded: their opt-<id>.md log marks them as hand-tuned.
    if (HERE/'optimization-log'/('opt-'+str(i)+'.md')).exists():
        print('skip optimized course',i,n['file'])
    else:
        (OUT/n['file']).write_text(doc)
# Keep the existing sample intact except for a direct path to the new learning home.
if 'href="index.html">学习首页' not in sample:
    SAMPLE.write_text(sample.replace('<a class="btn" href="../index.html">论文导航</a>','<a class="btn" href="index.html">学习首页</a><a class="btn" href="../index.html">论文导航</a>'))
for pi,m in enumerate(re.finditer(r'<section class="page" data-ch="(\d+)" data-t="([^"]+)">(.*?)</section>',sample,re.S),1):
    title=re.search(r'<h2[^>]*>(.*?)</h2>',m[3],re.S).group(1)
    syllabus.append([1,SAMPLE.name,pi,int(m[1]),m[2],re.sub('<[^>]*>','',title),'参考样例原有交互','参考课程原有出处','见页面'])
syllabus.sort(key=lambda row:(row[0],row[2]))
with (HERE/'syllabus.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['论文编号','课程文件','页','章','目录短名','断言标题','交互类型','出处','PDF页']);w.writerows(syllabus)
(WORK/'courses.json').write_text(J(all_data))
# Course metadata for the navigation page is inlined, ensuring file:// usage.
navdata=[{k:n[k] for k in ['id','zh','title','kind','claim','category','file','year']} for n in all_data]
# Title-only rows (no full text yet) join the map as external references, never as courses.
for i in sorted(PENDING):
    r=rows[i-1]
    navdata.append({'id':i,'zh':PENDING_ZH.get(i,r['论文题名']),'title':r['论文题名'],'kind':'待补全文','claim':'全文待补，暂无互动课程；先沿原站查看题录与摘要，全文入库后再补课。','category':r['分类'],'file':r['URL'],'year':r['年份']})
navtemplate=(HERE/'home.html').read_text();(OUT/'index.html').write_text(navtemplate.replace('/*__CATALOG__*/',J(navdata)))
for page in OUT.glob('*.html'):
    page.write_text(with_baidu_analytics(page.read_text()))
print(json.dumps({'courses':len(all_data),'new_courses':len(all_data)-1,'total_whiteboard_pages':len(syllabus),'briefs':str(WORK),'home':str(OUT/'index.html')},ensure_ascii=False))
