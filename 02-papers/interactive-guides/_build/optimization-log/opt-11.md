# opt-11 大模型辅助白帽SEO

- 文件：`02_GEO方法优化_White_Hat_Search_Engine_Optimization_using_LLMs.html`
- 审计发现：
  1. 证据读数页（p12）近乎空白：`PAPER.stats` 为空，只渲染通用「先读证据类型」文案加摘要原文；论文 Table 1（LambdaMARTComp）、Table 2（E5Comp）、Table 3（在线竞赛）的真实数值完全未呈现。
  2. 改动实验室（p11）无实质交互：只有「操作前/操作后」两句泛泛文案（「只追求更高排序忽略语义变化」），大片留白；论文最核心的机制——排序历史反馈 → 提示词改写 → 再排序的迭代循环，以及四类提示上下文（Pointwise/Pairwise/Listwise/Temporal）完全未呈现。
  3. 案例页（p18）无具体内容：`originalCases` 缺 id 11，页面只有方法概括句；论文 §2 的真实操作流程（共享提示词 + 上下文、GPT-4o 只输出改写稿、TrueTeacher/语料库双口径检查）未被转述。
  4. 自测 5 题为模板腔：第 1 题答案即 claim 原文，干扰项与论文无关（「网页颜色是否好看」），解释空泛。
  5. 发现页 finding_details 每条仅 25–33 字，4 条出处全标「摘要与研究目标 · PDF p.1」；发现页 b-key 与页面标题完全重复。
  6. 指标页（p7）专业层无公式：Scaled Promotion、OrigFaith（TrueTeacher 蕴含归一）、CorpFaith（前 10 篇双向均值）及置换检验口径缺失。
  7. 23 页讲稿全部为同一模板句；绝大多数 b-key 出处错标为「摘要与研究目标 · PDF p.1」。
  8. 封面右列「证据类型」卡只重复课程标题，零数字零信息量。
- 已做优化：
  1. **招牌交互「排序反馈 → 文档修改 → 再排序」循环演示**（p11 改动实验室）：左栏为 7 轮轮次条 + 5 文档排名列表（「你的文档」高亮、移动箭头）+ 当前排名与累计 Scaled Promotion 读数 + 忠实性仪表；右栏为四类提示类型选择（Pointwise 单项 / Pairwise 成对 / Listwise 列表 / Temporal 时序），切换后联动重演整条轨迹——「LLM 看到什么」上下文卡按附录 Figure 1–2 结构转述，改写区以红删绿增展示每轮改写示意，白帽约束常驻（只编辑影响最大的句子、≤150 词、与原文非常相似、TrueTeacher 单独评测忠实性，§2 · PDF p.1–2）。「下一轮」逐步推进「看排名 → 改写 → 重排」。轨迹按论文定性结论编码：Pairwise/Listwise 每轮升 1 名、Temporal 隔轮升、Pointwise 两轮升 1 名（§3 · PDF p.3），图注标明轨迹与忠实度曲线为教学示意、实测数值在证据读数页。全部 `<button>` + aria-pressed，动态区 aria-live，轮次条支持方向键（preventDefault 防翻页）。
  2. **证据读数页重写**（p12）：四个视图——表 1 LambdaMARTComp / 表 2 E5Comp / 表 3 在线竞赛 / 原文表格节选。每张表两张 HTML/CSS 图：Scaled Promotion 零轴发散条形图（SentReplace 基线灰、机器人蓝、学生浅蓝，数值标签含 U+2212 负号）；忠实性与质量对照图（OrigFaith / CorpFaith(E5) / CorpFaith(TF.IDF) 或 Q/R，虚线为同组学生参照）。数值逐格核对自 PDF Table 1/2/3（如 0.345 vs −0.095、0.341 vs −0.128、Q 0.911 vs 0.732、R 0.8 vs 0.642），出处标 Tables 1–3 · PDF p.3–4；图注写明显著性与两处例外（Pairwise 组质量 0.822 低于学生 0.925 但多数合格；其 CorpFaith(E5) 0.663 略低于 0.675）。专业层附四条公式（Scaled Promotion、RF、OrigFaith、CorpFaith）与检验细节（100,000 次置换、p < 0.05、GPT-4o、192 个配置）。
  3. **案例页收录论文真实操作流程**（p18）：`originalCases[11]` 加入 §2 · 附录 Figure 1–2 · §3 的中文转述（问题与输入：提示词两部分；操作与检查：GPT-4o 只输出改写稿、TrueTeacher 蕴含分数算 OrigFaith、语料库对照算 CorpFaith、≥3/5 标注者判定质量与相关性），右栏配本课构造的改写示意（红删绿增 + 检查清单），明确标注「示意未实测、未补造提升幅度」。
  4. **自测 5 题重写为论文专属**：核心机制（排名历史作隐式反馈，复习 p5）、反常发现（Listwise 质量评分 0.911 高于学生 0.732 且相关性更高，复习 p15）、指标理解（Scaled Promotion 定义，复习 p7）、适用边界（只测检索排序，迁移前先跑同口径对照，复习 p21）、证据局限（离线单轮快照、四类提示数值未全列出、学生不知情，复习 p8）；干扰项貌似合理（如「把 Scaled Promotion 换算成引用率」），每题解释给复习页码。
  5. **发现页深化**（p13–16）：finding_details 扩写到 55–75 字并补机制与数字；出处逐条改挂 `findingEv` 映射——F1 四类提示上下文（p.2）、F2 忠实性度量（p.2）、F3 Table 3（p.4）、F4 讨论与边界（p.4）；发现页 b-key 重写为具体结论（如「学生不知情时机器人仍提升排名与相关性」）。
  6. **专业层加深**：指标页（p7）三指标各有专属公式条（Scaled Promotion / OrigFaith / Q,R 判定口径）与置换检验注记；方法页（p10）三步各配论文细节——第一步四类上下文 2×2 卡（§2 · PDF p.2），第二步忠实性双口径（通俗层并行，专业层两条公式），第三步离线/在线两种验证设置（31 查询第 7 轮、15 查询第 4 轮、在线 15 新查询第 5–7 轮平均）。
  7. **文案与排版巡检**：全文无「不是…而是 / 并非…而是 / 不只是…而是」、无禁用词、无 emoji；新增文本数字与中文间加半角空格（如「150 词」「100,000 次」「p < 0.05」）；负号用 U+2212；23 页讲稿全部重写为页专属内容（2–3 句口语化）；b-key 出处逐页修正（§1、§2、§3 各节、Tables 1–3、Table 3、本课推断等）。
  8. **封面扩充**：`PAPER.stats` 扩为 4 个带口径与出处的关键数字（0.345 Pairwise 升幅 / 0.341 Listwise 升幅 / 0.8 在线竞赛相关性 / 192 个提示配置），替代原先只重复标题的卡片。
  9. 无障碍与新类名：新交互全部 `<button>` + aria-pressed + aria-live；新增 CSS/JS 一律 `x-` 前缀（x-loop / x-rounds / x-serp / x-doc / x-kpi / x-meter / x-prompt / x-diff / x-bar / x-track / x-fill / x-zero / x-group / x-typegrid / x-formula / x-case）；条形图为纯 HTML/CSS，无图表库、无外部请求；数据与表现分离（X_PROMPTS / X_NUM / X_METHOD / X_METRIC_PRO）。
- 验收：verify_one.py 全过——`pages=23, chapters=7, plain_overflow=[], pro_overflow=[], interaction_overflow=[], mobile_overflow=[], mobile_plain_overflow=[], missing_notes=[], errors=[], broken_links=[], quiz_complete=true, bytes=106021 (<200KB), pass=true`。另实测：循环交互逐轮推进与四类提示切换联动重演正确（Pairwise 第 4 轮到第 1 名、Pointwise 第 7 轮仅到第 2 名），零轴条形图与学生参照虚线正确，通俗/专业两模式 23 页逐页无溢出（含交互点击后状态），375px 无横向滚动，控制台零报错，`#p11` 深链接可用。
- 遗留：论文未公布四类提示的逐项数值（脚注 7 明示因篇幅省略），循环演示的排名轨迹与忠实度曲线为示意并已在页面标注，强弱次序以论文 §3 定性结论为准；表 1 中 SentReplace 组学生 Scaled Promotion 为 0.313（与机器人组学生为负不同），课程按表格原值呈现并保留「学生（基线组）」标签，口径差异需对照原文理解；离线/在线两套评估的学生 OrigFaith 数值不同（0.727 vs 0.821/0.865），课程分表呈现未跨表混用。
