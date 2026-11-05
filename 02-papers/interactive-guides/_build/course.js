/* PAPER CONTENT runtime. All paper-specific claims and values live in PAPER. */
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const ext=(u,t)=>`<a href="${esc(u)}" target="_blank" rel="noopener">${esc(t)}</a>`;
const src=e=>`<span class="src">${esc(e.label)} · PDF p.${e.page}</span>`;
const tip=t=>`<div class="caption">${esc(t)}</div>`;
const panel=(t,s)=>`<div class="answer"><div class="kicker">${esc(t)}</div><p>${esc(s)}</p></div>`;
const relatedLink=()=>`<a href="${esc(PAPER.related.url)}">${esc(PAPER.related.zh)}互动课</a> · ${ext(PAPER.related.pdf,'对照原文')}`;
const researchOnly=['理论框架','综述'].includes(PAPER.kind);
const stageNames=['问题与候选资料','研究干预与比较','答案或评价结果'];
const termHtml=()=>Object.entries(GLOSSARY).map(([k,g])=>`<button type="button" class="term" data-term="${k}">${esc(g.t)}</button>`).join(' · ');
const state={step:0,metric:0,num:0,lim:0,role:0,proof:0,q:0,answers:[],checks:new Set(),flips:new Set()};
function choices(labels,selected,action){return `<div class="choice-row" role="group">${labels.map((t,i)=>`<button type="button" class="choice" data-action="${action}" data-value="${i}" aria-pressed="${i===selected}">${esc(t)}</button>`).join('')}</div>`}
function dataNumbers(){return PAPER.stats.length?`<div class="number-grid">${PAPER.stats.slice(0,4).map(s=>`<div class="number-tile"><div class="number">${esc(s.v)}</div><div class="label">${esc(s.name)}</div>${tip(s.source)}</div>`).join('')}</div>`:`<div class="answer"><div class="kicker">证据类型 · ${esc(PAPER.kind)}</div><h3>${esc(PAPER.zh)}</h3><p>${esc(PAPER.kind_note)}</p>${tip('本篇未在封面展示未经逐项核对的效果数值。')}</div>`}
function flow(highlight){return `<div class="flow-line">${stageNames.map((t,i)=>`${i?'<span aria-hidden="true">→</span>':''}<div class="flow-node ${highlight===i?'active':''}">${esc(t)}<div class="caption">${esc(PAPER.steps[i])}</div></div>`).join('')}</div>`}
function sourceView(index=0){const e=PAPER.evidence[index%PAPER.evidence.length];return `<div class="source-text" lang="en">${esc(e.text)}</div>${src(e)}${tip('原文抽取节选，保留核验入口；完整方法与表格请查看原文。')}`}
const notesForStep=i=>[
 `输入与目标：${PAPER.question}。先明确数据单位与研究对象：${PAPER.setting}。`,
 `研究比较：${PAPER.steps[1]}。对照关系决定哪些变化能够归因于研究干预。`,
 `结果解读：${PAPER.steps[2]}。回到本篇结论：${PAPER.claim}。`
][i];
function draw(view){
 let h='';
 if(view==='cover')h=`<div class="columns wide"><div><div class="kicker">${esc(PAPER.kind)} · ${esc(PAPER.year)} · ${esc(PAPER.version)}</div><p class="intro">${esc(PAPER.claim)}</p><div class="english">${esc(PAPER.title)}</div><div class="muted" style="margin-bottom:12px">${esc(PAPER.authors.split("; ")[0])}${PAPER.authors.includes(";")?" 等":""} · 署名见引用抽屉</div><div class="muted">${ext(PAPER.url,'论文原站与署名')}${PAPER.pdf?' · '+ext(PAPER.pdf,'本地PDF'):''}</div><div class="choice-row" style="margin-top:20px"><button class="btn primary" type="button" data-go="2">开始上课 →</button><a class="btn" href="index.html">返回学习地图</a></div>${tip('按 ← → 翻页，M 切换深度，N 查看讲稿。进度自动保存在当前浏览器。')}</div>${dataNumbers()}</div>`;
 else if(view==='route')h=`<div class="columns"><div><ol class="fact-list"><li>${esc(PAPER.question)}</li><li>${esc(PAPER.metrics[0].name)}衡量什么？</li><li>${esc(PAPER.steps[1])}怎样起作用？</li><li>哪些条件会限制结论迁移？</li></ol><div class="term-row">${termHtml()}</div></div><ul class="route-list">${CHAPTERS.map((c,i)=>`<li><button type="button" data-go="${chPages(i+1)[0]+1}"><span>${esc(c.t)} · ${esc(c.d)}</span><small>进入 →</small></button></li>`).join('')}</ul></div>`;
 else if(view==='scene')h=`<div class="columns"><div><p class="intro">${esc(PAPER.query)}</p><p>同一目标下，先对照常见做法与研究启发。</p>${tip('以下为围绕论文方法构造的教学情境。不给示意操作附加实测收益。')}</div><div>${choices(['常见做法','研究启发'],0,'scene')}<div class="answer" id="sceneOut" aria-live="polite"><h3>常见做法</h3><p>${esc(PAPER.before)}</p>${tip('观察这一做法遗漏了什么条件。')}</div></div></div>`;
 else if(view==='concept')h=`${choices(PAPER.steps,0,'concept')}<div class="columns"><div class="answer" id="conceptOut" aria-live="polite"><h3>${esc(PAPER.steps[0])}</h3><p>${esc(notesForStep(0))}</p></div><div><div class="kicker">本篇要区分的量</div><ul class="fact-list">${PAPER.metrics.map((m,i)=>`<li><button type="button" class="term" data-term="metric${i}">${esc(m.name)}</button><small>${esc(m.plain)}</small></li>`).join('')}</ul></div></div>`;
 else if(view==='pipeline')h=`<div class="step-track">${PAPER.steps.map((s,i)=>`<button class="choice" type="button" data-action="step" data-value="${i}" aria-pressed="${i===state.step}">${esc(s)}</button>`).join('')}</div><div class="answer" id="stepOut" aria-live="polite"><h3>${esc(PAPER.steps[state.step])}</h3><p>${esc(notesForStep(state.step))}</p><div class="only-pro pro-note">${esc(PAPER.setting)}。证据范围：${esc(PAPER.boundary)}。</div></div><div class="choice-row" style="margin-top:14px"><button class="btn" type="button" data-action="prevStep" ${state.step===0?'disabled':''}>上一步</button><button class="btn" type="button" data-action="nextStep" ${state.step===PAPER.steps.length-1?'disabled':''}>下一步</button></div>${tip('流程按论文方法重新组织；箭头表达研究逻辑，不代表时间成本。')}`;
 else if(view==='boundary')h=`${choices(['研究输入','干预环节','结果口径'],1,'flow')}<div id="flowOut" aria-live="polite">${flow(1)}</div><div class="columns">${panel('能够支持',PAPER.claim)}${panel('适用边界',PAPER.boundary)}</div>`;
 else if(view==='metric')h=`<div class="columns"><div>${choices(PAPER.metrics.map(m=>m.name),state.metric,'metric')}<div class="answer" id="metricOut" aria-live="polite"><h3>${esc(PAPER.metrics[state.metric].name)}</h3><p class="only-plain">${esc(PAPER.metrics[state.metric].plain)}</p><div class="only-pro"><p>${esc(PAPER.metrics[state.metric].plain)}</p><div class="pro-note">先核对分母、样本单位、条件与聚合方式。${esc(PAPER.extra)}</div></div></div></div><div><div class="kicker">指标解释的检查次序</div><ul class="fact-list"><li>测量对象<small>${esc(PAPER.setting)}</small></li><li>对应结论<small>${esc(PAPER.findings[0])}</small></li><li>禁止越界<small>${esc(PAPER.boundary)}</small></li></ul></div></div>`;
 else if(view==='design')h=`<div class="columns"><div><div class="kicker">${esc(PAPER.kind)} · 研究设计</div><p class="intro">${esc(PAPER.setting)}</p><div class="callout">${esc(PAPER.boundary)}</div>${tip('研究类型会决定所需对照。综述需要核查纳入条件，理论需要核查假设，实证需要核查比较设计。')}</div><div>${choices(PAPER.evidence.map(e=>e.label),state.proof,'proof')}<div id="proofOut" aria-live="polite">${sourceView(state.proof)}</div></div></div>`;
 else if(view==='control')h=`<div class="columns"><div><div class="kicker">给你的复验方案做检查 · 本课推断</div><div class="check-list">${['保持研究问题和对象一致','明确基线与比较方案','记录引擎或数据版本','报告负向变化与不确定性'].map((s,i)=>`<button type="button" class="choice" data-action="check" data-value="${i}" aria-pressed="${state.checks.has(i)}"><span class="checkmark">${state.checks.has(i)?'✓':''}</span>${s}</button>`).join('')}</div></div><div class="answer" id="controlOut" aria-live="polite"><h3>${state.checks.size===4?'具备基本复验要素':'继续补齐比较条件'}</h3><p>${esc(PAPER.extra)}</p><div class="caption">勾选用于检查方案完整性，无法自动证明因果识别成立。</div><div class="only-pro pro-note">${esc(PAPER.boundary)}</div></div></div>`;
 else if(view==='method')h=`<div class="step-track">${PAPER.steps.map((s,i)=>`<button type="button" class="choice" data-action="method" data-value="${i}" aria-pressed="${i===0}">${esc(s)}</button>`).join('')}</div><div class="columns"><div class="answer" id="methodOut" aria-live="polite"><h3>${esc(PAPER.steps[0])}</h3><p>${esc(notesForStep(0))}</p><div class="callout">要检查：${esc(PAPER.findings[0])}。</div></div><div><div class="kicker">保持不变的约束</div><ul class="fact-list"><li>事实与来源可追溯</li><li>指标含义保持一致</li><li>${esc(PAPER.boundary)}</li></ul></div></div>`;
 else if(view==='lab')h=`${choices(['操作前','操作后','并排比较'],2,'lab')}<div id="labOut" aria-live="polite">${labHtml(2)}</div><div class="callout" style="margin-top:16px">对应方法：${esc(PAPER.steps.join(' → '))}</div>${tip('教学示意。前后文案为本课构造，未在原论文中测量效果。')}`;
 else if(view==='numbers')h=numbersHtml();
 else if(view.startsWith('finding')){const ix=+view.slice(-1);h=`<div class="ev" style="margin-bottom:16px">F${ix+1} · ${src(PAPER.evidence[0])} · 证据强度 <span class="${PAPER.strength==='弱'?'str-l':'str-m'}">${esc(PAPER.strength)}</span> ${esc(PAPER.strength_why)}</div><div class="columns"><div><p class="intro">${esc(PAPER.findings[ix])}</p>${choices(['论文发现','实践含义','适用条件'],0,'finding'+ix)}<div class="answer" id="findingOut${ix}" aria-live="polite"><p>${esc(PAPER.finding_details[ix])}</p><div class="caption">结合本篇研究设计理解这条发现。</div></div></div><div><div class="kicker">如何核查这一发现</div><ul class="fact-list"><li>研究设置<small>${esc(PAPER.setting)}</small></li><li>观察指标<small>${esc(PAPER.metrics[ix%PAPER.metrics.length].name)}：${esc(PAPER.metrics[ix%PAPER.metrics.length].plain)}</small></li><li>迁移约束<small>${esc(ix===3?PAPER.extra:PAPER.boundary)}</small></li></ul><button type="button" class="btn" data-go="8" style="margin-top:12px">回到原文证据 →</button></div></div>`;}
 else if(view==='compare')h=`${choices(['本篇研究','相关研究','对照启发'],0,'compare')}<div id="compareOut" aria-live="polite">${compareHtml(0)}</div>`;
 else if(view==='case')h=caseHtml();
 else if(view==='persona')h=personaHtml();
 else if(view==='mature')h=matureHtml();
 else if(view==='limits')h=`<div class="columns"><div>${choices(PAPER.limitations.map(l=>l[1]),state.lim,'limit')}</div><div class="answer" id="limitOut" aria-live="polite">${limitHtml(state.lim)}</div></div>`;
 else if(view==='quotes'){const quotes=[...PAPER.findings,'应用策略需要保留任务与证据条件','有效测量需要同时报告代价与边界'];h=`<div class="flips">${quotes.map((s,i)=>`<button type="button" class="flip-card" data-action="flip" data-value="${i}" aria-pressed="${state.flips.has(i)}"><b>${esc(s)}。</b><span class="flip-back">依据：${esc(i<4?PAPER.claim:PAPER.boundary)}<br>用法：${esc(i<3?PAPER.steps[i]:'记录口径并检查迁移条件')}。</span><small>本课提炼 · 点击查看依据</small></button>`).join('')}</div><div class="choice-row" style="margin-top:12px"><button class="btn" type="button" data-action="copySummary">复制要点与出处</button></div>`;}
 else if(view==='quiz')h=quizHtml();
 return h;
}
function labHtml(v){const a=panel('操作前 · 示意',PAPER.before),b=panel('操作后 · 示意',PAPER.after);return v===2?`<div class="two-docs">${a}${b}</div>`:v===0?a:b;}
function numbersHtml(){
 if(!PAPER.stats.length)return `<div class="columns"><div><p class="intro">先读证据类型，再决定该问哪些效果数字。</p><p>${esc(PAPER.claim)}</p>${choices(['研究支持','尚需验证'],0,'numberless')}<div class="callout" id="numberlessOut" aria-live="polite">${esc(PAPER.setting)}</div></div><div>${sourceView(0)}</div></div>`;
 const s=PAPER.stats[state.num];
 const chart=[17,46,68].includes(PAPER.id)?`<div class="only-pro"><div class="kicker">同口径数值对照 · 零点起算</div>${(PAPER.id===17?PAPER.stats.slice(1,4):PAPER.stats.slice(0,2)).map(x=>`<div class="bar-result"><span>${esc(x.name)}</span><div class="bar-track"><div class="bar-fill" style="width:${parseFloat(x.v)}%"></div></div><span>${esc(x.v)}</span></div>`).join('')}</div>`:'';
 return `${choices([...PAPER.stats.map(s=>s.name),'原文表格节选'],state.num,'number')}<div id="numberOut" aria-live="polite"><div class="columns"><div><div class="kicker">${esc(s.name)}</div><div class="number-large">${esc(s.v)}</div>${src({label:s.source,page:s.page})}</div><div class="answer"><h3>这个数字表示什么</h3><p>${esc(s.context)}</p><div class="caption">${esc(PAPER.extra)}</div></div></div>${chart}</div>`;
}
function compareHtml(v){
 if(v===0)return `<div class="columns">${panel(PAPER.zh,PAPER.claim)}${panel('证据边界',PAPER.boundary)}</div>`;
 if(v===1)return `<div class="answer"><h3>${esc(PAPER.related.zh)}</h3><p>${esc(PAPER.related.claim)}</p>${relatedLink()}${tip('按相关论文摘要转述；沿用该论文的研究范围。')}</div>`;
 return `<div class="answer"><h3>重新检查研究阶段与目标量</h3><p>${esc(PAPER.extra)}</p><p>对照阅读时记录：对象是否相同、来源是否已进入候选集、指标能否直接比较。</p>${relatedLink()}${tip('本段为教学推断。两篇论文的数字不宜直接相加。')}</div>`;
}
const originalCases={
 25:['争议问题是否有充分支持？','论文以阿斯巴甜与癌症关联等争议问题说明证据冲突。','比较真实网页中的事实、论证风格与相关性，观察模型回答变化。','Introduction / 摘要'],
 35:['虚构咖啡机目录中的产品如何排序？','论文分别观察很少被推荐与通常位列次选的目标产品。','控制商品目录后比较异常附加文本对首选概率的影响。','摘要 / Figure 1'],
 38:['消费商品推荐为何出现排序偏差？','来源正文被放入模型上下文，名称与位置也可能影响输出。','分别控制产品名、内容和位置，再比较推荐排序分布。','摘要 / Figure 1'],
 52:['合同的责任限制条款包括哪些内容？','句子级检索可能只取得损害类型，漏掉责任上限与例外。','层次节点保留完整条款，帮助同时回答责任限制和例外。','论文末尾 qualitative example'],
 58:['付费关联评测被答案采纳后需披露什么？','引文能够支持产品主张，但付费关联可能改变读者解释。','分别检查关系证据、答案采用、重要性和披露；缺证保持未决。','Introduction'],
 63:['背包是否符合短途旅行和工作装备需求？','卖方页面可能掩盖缺陷，让目标背包进入推荐集合。','以用户约束与效用评价结果，比较来源改写和防御前后。','Figure 1 / 摘要']};
function caseHtml(){const c=originalCases[PAPER.id];return `<div class="kicker">${c?'论文原例的中文转述':'依据方法构造的教学示意，尚未执行效果试验'}</div><p class="intro">${esc(c?c[0]:PAPER.query)}</p><div class="two-docs">${panel('问题与输入',c?c[1]:PAPER.before)}${panel('操作与检查',c?c[2]:PAPER.after)}</div><div class="callout" style="margin-top:16px">对应发现：${esc(PAPER.findings[0])}；${esc(PAPER.findings[2])}。</div>${tip(c?'出处：'+c[3]+'。本页未为案例补造提升幅度。':'原文完整案例请沿原文查看；本页仅解释方法，未将示意写成论文实测案例。')}`;}
function personaHtml(){const roles=['内容与业务负责人','技术与数据人员','研究与审核人员'];const todos=[['明确本页服务的具体需求：'+PAPER.query,'检查事实及来源，再尝试：'+PAPER.after,'保留未修改样本，对照观察：'+PAPER.metrics[0].name],['复现论文任务：'+PAPER.setting,'记录版本、候选来源与指标分母','分别追踪主指标和负向变化：'+PAPER.extra],['核对原文方法及结果的证据位置','检查研究边界：'+PAPER.boundary,'与《'+PAPER.related.zh+'》进行同口径对照']];return `${choices(roles,state.role,'role')}<div class="columns"><div><h3>${roles[state.role]}</h3><p style="margin-top:12px">为什么适合：${esc(state.role===0?PAPER.findings[0]:state.role===1?PAPER.findings[1]:PAPER.findings[3])}。</p><div class="callout warn">避免：${esc(PAPER.before)}后，直接宣称所有结果都由该操作带来。</div></div><div><ul class="fact-list">${todos[state.role].map((s,i)=>`<li>${esc(s)}<small>对应 F${state.role===0?1:state.role===1?2:4} · 本课应用推断</small></li>`).join('')}</ul></div></div>`;}
function matureHtml(){const forms=PAPER.kind==='风险研究'?['来源与关系审计表','红队测试用例库','防御上线复核单']:PAPER.category.startsWith('09')||PAPER.category.startsWith('08')?['检索运行追踪','技术基准卡','系统变更记录']:['带证据的说明文档','分层测量报告','可复现实验记录'];return `<div class="kicker">这一对应关系是本页的推断</div><table class="mini-table"><thead><tr><th>成熟形态</th><th>可观察的写法或字段</th><th>对应研究环节</th></tr></thead><tbody>${forms.map((s,i)=>`<tr><td>${esc(s)}</td><td>${esc([PAPER.query+'；事实、来源和适用条件',PAPER.metrics.map(m=>m.name).join('、')+'；按样本与版本分层','输入、操作、比较、负向结果和重测条件'][i])}</td><td>${esc(PAPER.steps[i])}</td></tr>`).join('')}</tbody></table><div class="${PAPER.kind==='风险研究'?'callout warn':'callout'}" style="margin-top:18px">${PAPER.kind==='风险研究'?'底线提示：仅在授权测试环境评估风险；公开课程聚焦识别、评估与防御。':'采用已有工作形态承接证据，先做小范围复验，再决定扩大应用。'}</div>`;}
function limitHtml(i){const l=PAPER.limitations[i];return `<span class="tag ${l[0]==='高'?'neg':'acc'}">影响${esc(l[0])}</span><h3>${esc(l[1])}</h3><p>${esc(l[2])}</p>${i===4?relatedLink():tip(i===0?'来自本篇研究范围与局限解读。':'本课审查提示，需结合原文进一步核验。')}`;}
function quizHtml(){
 const q=PAPER.quiz[state.q];
 if(!q){const score=state.answers.filter((a,i)=>a===PAPER.quiz[i].a).length;return `<div class="columns"><div><div class="kicker">自测完成</div><div class="number-large">${score} / ${PAPER.quiz.length}</div><p>按每题反馈回看对应页面，再继续学习。</p><div class="choice-row"><button class="btn" type="button" data-action="resetQuiz">重新作答</button><a class="btn" href="index.html">回学习地图</a></div></div><div>${panel('带走的结论',PAPER.claim)}<div class="caption">${ext(PAPER.url,'论文原文')} · ${relatedLink()}</div></div></div>`;}
 const a=state.answers[state.q];return `<div class="columns wide"><div><div class="kicker">第 ${state.q+1} 题 / 共 ${PAPER.quiz.length} 题</div><h3>${esc(q.q)}</h3><div class="quiz-options">${q.o.map((s,i)=>`<button type="button" class="choice ${a==null?'':i===q.a?'correct':i===a?'incorrect':''}" data-action="answer" data-value="${i}" ${a!=null?'disabled':''}>${esc(s)}</button>`).join('')}</div>${a!=null?`<div aria-live="polite" class="muted">${a===q.a?'回答正确。':'请回看对应证据。'}${esc(q.e)}<button type="button" class="term" data-go="${q.p}">复习第 ${q.p} 页</button></div><button class="btn primary" type="button" data-action="nextQuiz" style="margin-top:10px">${state.q===PAPER.quiz.length-1?'查看得分':'下一题'}</button>`:''}</div><div>${panel('自测的目的','辨别核心结论、指标含义、适用条件与证据强弱。答错会提供对应复习页。')}<div class="caption">${ext(PAPER.url,'打开原文核对')} · 可切换专业模式回看研究口径。</div></div></div>`;
}
function renderAll(){pages.forEach(p=>$('.lesson',p).innerHTML=draw(p.dataset.view));}
renderAll();
// Existing HTML owns layout; delegated events update only the affected learning activity.
function selectIn(b){$$('button',b.parentElement).forEach(x=>x.setAttribute('aria-pressed',x===b));}
document.addEventListener('click',e=>{
 const b=e.target.closest('[data-action]');if(!b)return;const v=+(b.dataset.value||0),a=b.dataset.action;
 const box=b.closest('.lesson');const p=b.closest('.page');
 if(['scene','concept','method','flow','lab','compare','numberless','proof','number','metric','limit'].includes(a)||a.startsWith('finding'))selectIn(b);
 if(a==='scene')$('#sceneOut').innerHTML=`<h3>${v?'研究启发':'常见做法'}</h3><p>${esc(v?PAPER.after:PAPER.before)}</p>${tip(v?'本课应用推断。需要在目标场景中验证。':'教学示意，尚未进行实际效果测量。')}`;
 else if(a==='concept')$('#conceptOut').innerHTML=`<h3>${esc(PAPER.steps[v])}</h3><p>${esc(notesForStep(v))}</p>`;
 else if(a==='step'||a==='prevStep'||a==='nextStep'){state.step=a==='step'?v:Math.max(0,Math.min(PAPER.steps.length-1,state.step+(a==='nextStep'?1:-1)));box.innerHTML=draw('pipeline');}
 else if(a==='flow')$('#flowOut').innerHTML=flow(v);
 else if(a==='metric'){state.metric=v;const m=PAPER.metrics[v];$('#metricOut').innerHTML=`<h3>${esc(m.name)}</h3><p>${esc(m.plain)}</p><div class="only-pro pro-note">${esc(PAPER.extra)}</div>`;}
 else if(a==='proof'){state.proof=v;$('#proofOut').innerHTML=sourceView(v);}
 else if(a==='check'){state.checks.has(v)?state.checks.delete(v):state.checks.add(v);box.innerHTML=draw('control');}
 else if(a==='method')$('#methodOut').innerHTML=`<h3>${esc(PAPER.steps[v])}</h3><p>${esc(notesForStep(v))}</p><div class="callout">核对发现：${esc(PAPER.findings[v])}。</div>`;
 else if(a==='lab')$('#labOut').innerHTML=labHtml(v);
 else if(a==='numberless')$('#numberlessOut').textContent=v?PAPER.boundary:PAPER.setting;
 else if(a==='number'){
  if(v===PAPER.stats.length){const t=PAPER.table;$('#numberOut').innerHTML=t?`<div class="source-text table" lang="en">${esc(t.text)}</div>${src(t)}${tip('版面抽取节选，换行可能影响列对齐；完整表格及脚注以PDF为准。')}`:`<div class="answer"><p>未找到可可靠定位的首张表格。保留已核对的摘要数值，完整结果请打开原文。</p>${ext(PAPER.url,'查看原文')}</div>`;}
  else{state.num=v;const s=PAPER.stats[v];$('#numberOut').innerHTML=`<div class="columns"><div><div class="kicker">${esc(s.name)}</div><div class="number-large">${esc(s.v)}</div>${src({label:s.source,page:s.page})}</div><div class="answer"><h3>这个数字表示什么</h3><p>${esc(s.context)}</p>${tip(PAPER.extra)}</div></div>`;}}
 else if(a.startsWith('finding')){const ix=+a.slice(-1);$('#findingOut'+ix).innerHTML=`<p>${esc(v===0?PAPER.finding_details[ix]:v===1?'应用推断：'+PAPER.steps[ix%PAPER.steps.length]+'，并以'+PAPER.metrics[ix%PAPER.metrics.length].name+'检验。':PAPER.boundary)}</p>${tip(v===1?'行动建议属于教学推断。':v===2?PAPER.extra:'需要连同研究设计解读，勿省略条件。')}`;}
 else if(a==='compare')$('#compareOut').innerHTML=compareHtml(v);
 else if(a==='role'){state.role=v;box.innerHTML=personaHtml();}
 else if(a==='limit'){state.lim=v;$('#limitOut').innerHTML=limitHtml(v);}
 else if(a==='flip'){state.flips.has(v)?state.flips.delete(v):state.flips.add(v);b.setAttribute('aria-pressed',state.flips.has(v));}
 else if(a==='copySummary')copyText(PAPER.findings.map(t=>t+'。').join('\n')+'\n来源：'+PAPER.title+' · '+PAPER.version+'\n'+PAPER.url+'\n边界：'+PAPER.boundary);
 else if(a==='answer'&&state.answers[state.q]==null){state.answers[state.q]=v;box.innerHTML=quizHtml();}
 else if(a==='nextQuiz'){state.q++;box.innerHTML=quizHtml();}
 else if(a==='resetQuiz'){state.q=0;state.answers=[];box.innerHTML=quizHtml();}
 // Preserve keyboard continuity after components render fresh buttons.
 if(!b.isConnected){const replacement=box.querySelector(`[data-action="${a}"][data-value="${v}"]`)||box.querySelector('[data-action]');if(replacement)replacement.focus({preventScroll:true});}
 checkOverflow(pages.indexOf(p));
});
// Arrow keys within a choice group change that activity, and leave slide navigation untouched.
document.addEventListener('keydown',e=>{
 const b=e.target.closest('.lesson .choice-row button,.lesson .step-track button');
 if(!b||!['ArrowLeft','ArrowRight'].includes(e.key))return;
 e.preventDefault();e.stopImmediatePropagation();const group=b.parentElement,bs=$$('button',group);const ix=(bs.indexOf(b)+(e.key==='ArrowRight'?1:-1)+bs.length)%bs.length;bs[ix].click();if(bs[ix].isConnected)bs[ix].focus();
},true);
