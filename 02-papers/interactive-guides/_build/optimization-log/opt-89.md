# opt-89 随机游走链接分析（SALSA 与 TKC 效应）

- 文件：`13_链接分析与外链理论_C07_The_Stochastic_Approach_for_Link_Structure_Analysis_SALSA_and_the_TKC_Effect.html`（89,777 B → 102,431 B，上限 200 KB）
- 论文：The Stochastic Approach for Link-Structure Analysis (SALSA) and the TKC Effect（Lempel & Moran；WWW9 2000 会议版 → ACM TOIS 19(2) 2001 期刊扩展版；理论框架）

## 审计发现（Playwright 1440×900 无头 Chromium，优化前截图 23 页至 /tmp/opt-89/before/，两种模式 PGS.checkAll() 均为空）

1. 空壳模板课：23 页全由通用 runtime 渲染，无论文专属交互；第 11 页「改动实验室」只有两行 before/after 面板，整页大半空白（截图确认）。
2. 论文原例缺席：`originalCases` 没有 id 89，案例页写着「原文完整案例请沿原文查看」，但论文 §5.2 自带 4 个带表格的真实查询案例（java/EarthWeb、movies/go.msn.com、abortion、censorship Table I），一个都没用。
3. 证据读数页无图：4 个数字卡孤立展示，无可视对比；Table I 有互强化 vs SALSA 的可比权重、Table II/III/V/VI 有可清点的「前 10 名被谁占据」数据，全部缺席；`chart` 变量只对 id 17/46/68 生效，本课无图。
4. 自测模板腔：Q1 正确项是 60 字整句 claim，Q3 干扰项「网页颜色是否好看」「作者是否知名」与本篇无关，解释无出处。
5. 专业层名不副实：指标页 only-pro 只有一句「先核对分母…」；命题 5（p_i = d_in(i)/W）、命题 1/2（Ck 构造）、命题 6（分量规模占比）、二部图定义均未出现。
6. 23 页讲稿是同一句「这一页围绕……展开…」；23 个 b-key 出处全部误标「摘要与研究目标 · PDF p.1」（如发现 3 的真实出处是 §5.2 Table VI · PDF p.18-19）。
7. 发现页证据行固定引用 evidence[0]（摘要），F2/F3/F4 未对应各自表格出处；PAPER.evidence 三条中两条几乎重复。
8. 引用抽屉 BibTeX 有坏数据：`year = {期刊扩展版）}`；版本标注「WWW 2000 / Computer Networks」与实际（TOIS 2001）不符。

## 已做优化

1. **签名交互（第 11 页「改动实验室」，标题改为「同一个页面集，两种算法选出不同的权威」）**：新增 `x-` 前缀 TKC 对照实验室——SVG 示意拓扑按论文 §5.1 的 Ck 构造缩小重绘（小团体 3 枢纽 × 3 权威完全互链 = 9 边；大社区 10 枢纽各只指向 5 权威中的 2 个 = 20 边；3 个噪声枢纽跨社区连接），切「互强化法（Kleinberg）/ 随机游走法（SALSA）」两个按钮实时重算并重绘：右侧权威分前 6 名横条（小团体橙 / 大社区蓝，两算法共用同一比例，前 3 名描边加粗）、胜出社区 SVG 框加亮并标「前 3 多数」、结论一行 + 机制解读（专业层给命题 2/命题 1 与命题 5 出处）。分数由页面真实计算（HITS 幂迭代 600 轮 / SALSA 按命题 5 取带权入度占比），浏览器结果与 Python 参照逐位一致（HITS：小团体各 21.0% 对大社区最高 9.0%；SALSA：大社区前三各 14.3%，小团体 11.4% 并列第 4 名起）；拓扑按 Ck 构造缩小、两类权威入度只差一条边，图注全程标「机制示意」。按钮均为 `.choice`（choice-row 内），aria-pressed + aria-live 齐全，组件内方向键由既有 preventDefault 处理器接管（已实测不触发翻页）。
2. **证据读数页（第 12 页）**：新增「小团体垄断度」视图——java/movies/abortion 三查询的「前 10 名中站点群（或单一立场）页面数」双条形对照（互强化 10/10 对 SALSA 3/10、0/10、4/10），逐条带 Table II/III·V/VI 出处与清点口径说明，标注条长基线为 0；4 个数字卡保留并补专业层口径（1999 年 2 月 AltaVista 快照）。
3. **案例页（第 18 页）改为论文原例**：`originalCases` 加入 id 89——java 查询：互强化前 10 名全是 EarthWeb Inc. 站点群（jars.com、gamelan.com、datamation.com 等，域名不同致域内过滤未拦住），SALSA 同一页面集只保留 3 席并换入 java.sun.com、javaworld.com、sun.com；出处 §5.2 Table II · PDF p.17，声明未补造提升幅度。
4. **自测重写 5 题**：核心结论（两条马尔可夫链的随机游走）、TKC 机制（movies/go.msn.com 封闭互链）、指标理解（带权入度 ÷ 总边权，干扰项含 W^T W 主特征向量）、适用边界（建图三步在前、只保证前 10 精度）、局限（出链灌水）；干扰项貌似合理且贴近论文（如「权重统一设 0.85」暗扣 PageRank），每题解释带小节出处与复习页码（5/14/13/21/16），复习页码已实测可跳转。
5. **发现页 4 条**：证据行改为按发现映射原文节选（F1→命题 5 p.22、F2→TKC 定义 p.12、F3→abortion 案例 p.18、F4→出链灌水 p.25）；「实践含义」改为论文专属动作（独立来源域审计、前 10 名同站占比监控、两侧声音检查、枢纽维度先看根集隔离）。
6. **专业层加深**：指标页扩为 4 条指标（SALSA 权威分/枢纽分/互强化权威分/TKC 效应），only-pro 给命题 5 公式 p_i=d_in(i)/W 与命题 6 分量口径，右栏加两算法口径对照表；方法页/流程页每步配论文口径（三条过滤启发式、二部图与归一化矩阵乘积、命题 5/6）；概念页改为 4 张概念卡（枢纽与权威/二部图/两条随机游走/主社区），专业层带 §4.1 定义。
7. **PAPER 数据重写**：metrics 2→4 条（各带 plain/pro/src）；evidence 重写为 9 条互不重复的原文节选（p.1/10/12/14/16/18×2/22/25），实验设计页变成 9 段论证链切换器；新增 monopoly（3 查询清点）与 quotes（6 条金句卡，正面 + 背面依据与用法）；limitations 重写为 6 条论文专属（1999 年快照[高]、只看链接结构[高]、过滤启发式[中]、5 查询无盲评[中]、主机级降权局限[中]、两版本差异[低]）；strength_why 写实；新增 STEP_PLAIN/PRO、CONCEPTS、FIND_ACT、CHECKS、ROLES、成熟形态三行（外链来源审计表/建图口径文档/双算法对照报告）；GLOSSARY 换入互强化法、二部图、主社区、信息链接、根集、马尔可夫链。
8. **其余页面专属化**：对照检查页 4 项改为建图口径/过滤规则/双算法/前 10 名精度并各附论文做法；角色清单按三角色重写（为什么适合 + 3 条动词开头 + 避免）；场景页、研究位置页、研究对照页、要点卡复制按钮同步更新。
9. **文案与讲稿巡检**：23 页讲稿全部重写为真实讲稿（每页 2-3 句，含操作指引与证据提醒）；23 个 b-key 全部改为带正确出处的断言句（出处精确到小节与 PDF 页码）；9 个页面标题改为断言句；全文检索 `不是…而是 / 并非…而是 / 不只是…而是`、禁用词（赋能/抓手/闭环/颠覆/革命性/重磅/震撼）、emoji 均无；数字与中文间半角空格已核；无 eval、无新增外部请求、innerHTML 只拼接常量与运行时计算值。
10. **约束核对**：PGS core 两段与外壳骨架未动；23 页 `data-ch/data-t/data-view` 与 `.notes` 存在性不变；quiz 5 题 answer/nextQuiz/resetQuiz 流程不变；新增 CSS/JS 类名全部 `x-` 前缀；引用抽屉修正 BibTeX 年份（2001，会议版 2000）与版本标注（ACM TOIS 19(2) 2001 · 扩展自 WWW9 2000），meta paper-guide-source 同步。

## 验收（verify_one.py 最终输出）

```json
{"pages": 23, "chapters": 7, "plain_overflow": [], "pro_overflow": [],
 "missing_notes": [], "quiz_complete": true, "interaction_overflow": [],
 "mobile_overflow": [], "mobile_plain_overflow": [], "errors": [],
 "broken_links": [], "bytes": 102431, "pass": true}
```

另做人工功能核验（Playwright，/tmp/opt-89/func_check.py）：TKC 实验室 HITS→SALSA→HITS 三态往返，排名与结论逐次翻转且与 Python 参照一致；组件内方向键切换算法不触发翻页；证据读数 6 视图、概念 4 卡、案例页原例、发现页 4 出处、自测全流程（含复习页码）；专业模式实验室无溢出；控制台零报错；关键页截图复查（/tmp/opt-89/final、/tmp/opt-89/final2）。

## 遗留

- 招牌交互的拓扑是论文 §5.1 Ck 构造（k=3，n=16、m=4、C(n,k) 个枢纽）的缩小重绘版，已逐处标注「机制示意」；两命题的定性结论（命题 1/2）在缩小版上经实算复核成立，但未复现原构造的精确组合数。
- SALSA 主社区在第 12 页表格节选仅收录 Table I（censorship）；java/movies/abortion 的逐 URL 表未全文收录，完整列表需沿 PDF p.17-19 查看。
- 期刊版与会议版的命题编号差异未逐条比对（课程以 TOIS 2001 为准，已在批判阅读页提示）。
