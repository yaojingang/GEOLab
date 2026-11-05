# opt-90 主题敏感的 PageRank

- 文件：`13_链接分析与外链理论_C08_Topic_Sensitive_PageRank.html`
- 审计发现：
  1. 改动实验室（p11）无实质交互：只有「操作前/操作后」两块泛泛示意卡（外链策略 before/after），大片留白；论文最核心的机制——查询时按主题概率加权合成 16 个有偏向量——没有可探索的演示。
  2. 证据读数页（p12）只有单个大数字卡轮换，0.276 与 0.512 这对可比均值没有画成带基线的横条图；左上留白近半版。
  3. 出处页码系统性错误：`PAPER.stats` 四个数字全部标「PDF p.1」，实际 16 向量为 §3.2（p.2）、120 million 为 §4（p.4）、0.512/0.276 为 Figure 1（p.7）；4 条发现页与多数 b-key 一律标「摘要与研究目标 · PDF p.1」。
  4. 案例页（p18）写成「依据方法构造的教学示意」，而论文有真实定性案例：查询词 blues 在音乐页/产后抑郁页两种上下文分别命中 Arts 与 Health 向量（§4.4 · Table 8-9），`originalCases` 缺 id 90。
  5. 自测 5 题为模板腔：第 1 题答案即 claim 整句照抄，干扰项荒诞（「网页颜色是否好看」「作者是否知名」），解释空泛无机制。
  6. 专业层零公式：Eq 5（Rank=(1−α)M×Rank+α·p）、Eq 6（vj(i)=1/|Tj|）、Eq 7（P(cj|q′)∝P(cj)·∏P(q′i|cj)）、Eq 8（sqd=ΣP(cj|q′)·rankjd）与 OSim 定义（|A∩B|/n，n=20）均未出现；`PAPER.evidence[1]` 是摘要重复片段，用户实验与 blues 原例两段真证据缺席。
  7. 23 页讲稿全部为同一模板句；F2 细节只写「重叠度 0.04–0.13」，漏掉 Table 3「最相似对（Games, Sports）OSim 也只有 0.18」与 Table 2「换 α 影响更小」的对照锚点。
  8. 文案本身干净：无「不是…而是」句式、无禁用词、无 emoji、数字空格合规（此项为通过项）。
- 已做优化：
  1. **招牌交互「主题向量合成滑杆」**（p11）：查询词 blues（论文 §4.4 原例），三个论文锚点预设按钮——音乐页（Arts）/ 抑郁页（Health）/ 无偏置（NoBias），加 P(Arts|上下文)、P(Health|上下文) 两根滑杆（余量自动归一，互斥钳制）；右侧 6 个候选页实时重排——候选页取自论文 Table 9 真实结果（Arts 向量前 2：Britannica、BandHunt；Health 前 2：Northern County、Seasonal Affective Disorder；NoBias 第 1：TUCOWS），每行三色堆叠条（蓝=Arts 贡献、绿=Health、橙=通用余量，条长即合成分），▲▼ 标注相对无偏置基线的名次变化；权重读数与排名区 aria-live。默认状态即「音乐页上下文」＝论文 Arts 结果。图注注明向量给分为 0-100 示意值、候选页名次关系来自 Table 9（PDF p.9）；专业层给合成公式（Eq 8 · PDF p.3）、随机游走解释（α·P(cj|q′) 跳入 Tj · §3.3）与「实验只取 P(cj|q) 最高 3 个主题」（§4.3）。
  2. **证据读数页重写**（p12）：选中「主题敏感平均精度/无偏置平均精度」时显示 0.276 vs 0.512 带基线横条图（零点起算、灰=无偏置基线、蓝=主题敏感），图注写明口径（URL 被 ≥3/5 名志愿者判为相关才计入 · §4.3）与相对提升 +85.5%（按 0.512/0.276 − 1 换算）；「主题敏感向量数」视图补 16 个 ODP 顶级类目标签（出处 Table 4 表头 · p.5）；「抓取页面规模」补「含 ODP 300 万条 URL 中约 28 万条」（§4 · p.4）；专业层常驻注记：α 灵敏度（Table 2：α=0.05 与 0.25 平均 OSim 0.57-0.78，统一取 α=0.25）、主题向量差异（Table 3/4：最相似对 OSim 0.18，其余 0.04-0.13）、top-3 合成口径。
  3. **案例页收录论文原例**（p18）：`originalCases[90]` 加入 blues 双上下文案例（Table 8 两个真实上下文页 → Table 9 三列结果：Arts 全音乐站、Health 全抑郁相关页、NoBias 混入 baseball 与 MP3 站），出处 §4.4 · Table 8-9 · PDF p.7-9，注明未为案例补造提升幅度。
  4. **自测 5 题重写为论文专属**：查询时合成机制（Eq 8，复习 p5/p10）、主题向量差异的反常发现（最相似对 OSim 仅 0.18 且 α 影响更小，复习 p14）、OSim 口径辨析（对照 P@10 与 KSim，复习 p7）、迁移姿势（同主题引用为方向性启发需实测，复习 p21）、用户实验局限（10 查询 × 5 志愿者、≥3/5 判相关、未叠加文本信号，复习 p13）；干扰项均为貌似合理的机制性错误（如 HITS 重跑、开方压缩、上千名用户）。
  5. **发现页深化**（p13-16）：finding_details 扩写并补齐证据链——F1 加 Table 7 的 8/10 多数偏好与 hiv、shakespeare 两个例外；F2 加 Table 3 最相似对 0.18 与 Table 2 α 对照；F3 改写为 blues 原例复述；F4 补 top-3 合成口径；出处逐条改为 Figure 1 · Table 7（p.7）、Table 2-4（p.5）、§4.4 · Table 8-9（p.7-9）、§3.2-3.3（p.2-3）；「观察指标」改为各发现专属口径（不再 OSim/偏置系数轮换错配）。
  6. **专业层加深**：指标页（p7）OSim 补公式 OSim(τ1,τ2)=|A∩B|/n、n=20 与 KSim 口径（§4.1 · p.4），偏置系数补 Eq 5-6 与 α=0.25（p.2、p.4-5）；方法页（p10）三步各配专业层注记（Eq 5-6 含「非事后处理」提醒、Eq 7 unigram 语言模型与可换用户先验、Eq 8 与随机游走等价 + top-3 口径）；流程页（p5）专业层补合成公式一行。
  7. **证据数据修正**：`PAPER.stats` 四项出处页码全部改正（§3.2 p.2 / §4 p.4 / Figure 1 p.7 ×2）并补口径；`PAPER.evidence[1]` 由摘要重复片段替换为 §4.3 用户实验方法原文（10 查询、5 志愿者、≥3/5 判相关，p.5），新增 §4.4 blues 原例原文节选（p.7）——设计页（p8）证据标签从 2 个变 3 个。
  8. **讲稿与要点巡检**：重写 12 页讲稿（p5、7、8、10、11、12、13、14、15、16、18、23）为页专属口语化内容；11 个 b-key 出处逐页修正，p11/p18 的 b-key 重写为与新增内容匹配的断言（「同一查询词在不同主题上下文下排名不同：候选页与名次关系来自论文 Table 9」等）。
  9. **约束遵守**：PGS core 两段与外壳结构未动；23 页页数、data-ch/data-t/data-view、.notes 均保持；新 CSS/JS 全部 `x-` 前缀（x-mix / x-mix-row / x-mix-bar / x-mix-rows / x-mix-slider / x-mix-w / x-numbars）；预设按钮为 `<button>` + aria-pressed 并入 choice-row 方向键组，滑杆为原生 input[type=range]（全局方向键翻页对 input 自动让路），动态区 aria-live="polite"；无 eval、无外部请求、innerHTML 仅拼接常量与 esc() 后的数据。
- 验收：verify_one.py 全过——`pages=23, chapters=7, plain_overflow=[], pro_overflow=[], interaction_overflow=[], mobile_overflow=[], mobile_plain_overflow=[], missing_notes=[], errors=[], broken_links=[], quiz_complete=true, bytes=98351 (<200KB), pass=true`。另实测截图核对：招牌交互三预设联动重排正确（音乐页预设下 Britannica ▲3、TUCOWS ▼2；滑杆 0.45/0.45 时两主题页面交错、TUCOWS ▼5），条形图三色段与合成分一致，证据读数条形图基线与 +85.5% 标注正确，案例页/自测页/专业层公式渲染正常，通俗与专业两模式逐页无溢出，375px 无横向滚动，控制台零报错。
- 遗留：候选 6 页只覆盖 Table 9 三列的前几名（Arts 第 3 名 Artist Information、Health 第 3 名 Women's Mental Health、NoBias 第 2/3/5 名未纳入），页面已注明「候选 6 页取自 Table 9」；三个向量给每页的 0-100 分为示意值（论文只给名次不给分数），图注已标注；课程沿用论文 WWW 2002 版本口径（任务描述中「Haveliwala 2003」与本地 PDF 署名 WWW2002 不符，以 PDF 为准）。
