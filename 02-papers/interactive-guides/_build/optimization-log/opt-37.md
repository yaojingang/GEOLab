# opt-37 多方污染的PoisonArena

- 文件：`06_风险操纵_PoisonArena_Competing_Poisoning_Attacks_in_RAG.html`（84,383 B → 100,385 B，上限 200 KB）
- 论文：PoisonArena: Uncovering Competing Poisoning Attacks in RAG（arXiv:2505.12574v4，2025-06；首个多方竞争污染基准：7 种污染方法 × 单方/两两/3-4 方竞争，Bradley-Terry 竞争系数 θ，NQ + MS MARCO）

## 审计发现（Playwright 1440×900 无头 Chromium，截图 23 页至 /tmp/opt-37/，两种模式 PGS.checkAll()；verify 基线本就全过——模板空壳无溢出）

1. 空壳模板：23 页全由通用 runtime 渲染，无论文专属交互；「改动实验室」只是 before/after 各一句话。
2. 论文数据完全缺席：`PAPER.stats` 为空数组、`PAPER.table` 为 null，证据读数页只显示一句证据类型卡；论文 Table 1（单方 ASR/F1）、Table 2（s-ASR/m-ASR/s-F1/m-F1/θ 五指标）、Table 11（21 组两两对局）的数字一个都没进课程。
3. 核心卖点「单方口径失真」无从体验：论文点名的反常对局（黑盒 P-RAG 单方高出 AdvDecoding 20 多个百分点、正面对抗却落败）没有任何可操作演示。
4. 案例页 `originalCases` 无 id 37，只重复 before/after 模板句；而论文 Figure 1（p.2）有现成的总统辩论三方互斥注入案例。
5. 自测五题全部模板腔（「网页颜色是否好看」式凑数干扰项），解释无出处。
6. `finding_details` 每条 25-30 字（<40 字下限），无机制无数字；发现页证据出处一律笼统标「摘要与研究目标 · PDF p.1」；evidence[1]（p.6）文本截断在「It can be obser」且混入版面乱码。
7. 指标页专业层只有一句「先核对分母」；BT 概率公式（式 1 · p.5）、m-ASR 口径（附录 B.4.1 · p.16）缺席。
8. 23 页讲稿是同一句模板；b-key 出处几乎全部误标「摘要与研究目标 · PDF p.1」。

## 已做优化

1. **签名交互（第 11 页「改动实验室」→ 竞技场对局）**：新增 `x-` 前缀「单方 ASR vs 同场对抗 ASR」双口径对局演示——两行 7 方法 chips 任选攻击方与对手，左右两组零基线横条（数据条带数值标签）分别给出单方 ASR（Table 1 · PDF p.6）与两两对抗 ASR（Table 11 · PDF p.29，LLaMA-3-8B）；判定框自动输出「口径翻转」徽标与胜负差（如默认对局：单方 P-RAG 黑盒领先 24.8 个百分点，对抗却 AdvDecoding 39.3% 对 34.0% 胜出），论文点名的对局附专属注解（F1 0.66 对 0.34 等）；专业层实时按 θ 换算 BT 胜率 P=e^θ₁/(e^θ₁+e^θ₂) 并注明口径差异。同方法对局有守卫提示；按钮 aria-pressed、动态区 aria-live、组内 ←→ 键 preventDefault。
2. **证据读数页（第 12 页）重写**：填入论文五指标（s-ASR/m-ASR/s-F1/m-F1/θ，Table 2 · PDF p.9）——左栏 chips 选方法，显示「单方 → 竞争 ASR」大数字对、口径解释与完整五指标专业层（含附录 B.4.1 口径 · p.16）；右栏七方法同表对照表（单方/竞争 ASR 双色横条从零起算 + θ 列），选中行高亮。封面数字卡同步改为四张「单方 → 竞争」落差卡（84.2%→12.3% 等，带出处）。
3. **案例页（第 18 页）**：`originalCases` 新增 id 37——论文 Figure 1 原例中文转述：总统辩论问题下三方互斥叙事（亲拜登/亲特朗普/RFK Jr.）同时注入同一语料库，冲突上下文相互稀释或抵消，答案在多个选项间摇摆；标注 Figure 1 · PDF p.2，未为案例补造数字。
4. **自测重写 5 题**：核心结论（单方 ASR 不预测竞争）、反常对局（黑盒 P-RAG vs AdvDecoding，干扰项含「GASLITE 被击败」「ContentPoison 保持 36%」的事实反转）、θ 的来历与含义（式 1，干扰项含「归一化 ASR」）、ContentPoison 坍缩（36%→跌破 10%→趋近零）、迁移边界（对手集合绑定 + ICL 防御改变竞争格局，干扰项含「θ 是常数」「MS MARCO 无效」）；每题解释带 PDF 页码出处与复习页码（12/14/7/15/21）。
5. **发现页（13-16 页）**：4 条 `finding_details` 扩写至 55-90 字并嵌入论文数字（34.0% 对 39.3%、F1 0.34 对 0.66、36.0%→0.75%、1,000 轮模拟、θ=1.69）；b-key 改为带真实出处的断言（Figure 1 p.2、§4.3 p.7、p.8-9、§3-4 p.5-9）。
6. **指标页专业层（第 7 页）**：补 s-ASR/m-ASR 完整口径（附录 B.4.1 · PDF p.16，判定用子串匹配 + GPT-3.5 评审、人工抽检误差 2%-5%）与 BT 公式卡 `P(Aᵢ≻Aⱼ)=e^θᵢ/(e^θᵢ+e^θⱼ)`（式 1 · PDF p.5），切换 chips 后公式保持。
7. **证据节选修复与扩充**：evidence[1]（p.6）清除版面乱码、补全 Table 1 全部 7 行数字；新增第 4 条证据「竞争协议与模型」（式 1 与模拟四步 · PDF p.5），实验设计页（第 8 页）变为 4 视图可切换证据库。
8. **文案与讲稿巡检**：12 页讲稿重写为真实讲稿（封面/问题场景/流程/指标/设计/方法/竞技场/证据读数/4 条发现/案例/自测）；相关 b-key 出处全部改指真实位置；`不是…而是 / 并非…而是`、禁用词（赋能/抓手/闭环/颠覆/革命性/重磅/震撼）检索均无；数字与中文间半角空格（20 多个百分点、1,000 轮等）；无 emoji（仅保留外壳原有 ☰/✓ 功能字符）；无 eval、无新增外部请求。
9. **约束核对**：PGS core 两段未动（所有改动位于 PAPER 数据区、课程专用 CSS 与 PAPER CONTENT runtime）；外壳骨架未动；23 页 `data-ch/data-t/data-view` 与 `.notes` 存在性不变；quiz 5 题 answer/nextQuiz/resetQuiz 流程不变；新类名全部 `x-` 前缀（x-arena 相关：x-cols/x-duel-grid/x-verdict/x-numrow/x-numfill/x-t2/x-tdbar/x-chips/x-pair/x-note/x-flipbadge）。

## 验收（verify_one.py 最终输出）

```json
{"bytes": 100385, "pages": 23, "chapters": 7,
 "plain_overflow": [], "pro_overflow": [], "missing_notes": [],
 "quiz_complete": true, "interaction_overflow": [],
 "mobile_overflow": [], "mobile_plain_overflow": [],
 "errors": [], "broken_links": [], "pass": true}
```

## 遗留

- Table 11 的 F1 列未做成对展示（对局页只带 ASR 条，F1 以论文点名对局注解形式给出 0.66/0.34、0.64/0.36、0.73/0.27 三组），如需可再加 F1 切换维度。
- 竞争系数 θ 取自 Table 2 主设置（NQ · LLaMA-3-8B）；MS MARCO 与知识库攻击设置（Table 4/5/6）的数字未纳入交互，仅作为自测边界题的出处提及。
- 数字核对基于 pdftotext 版面抽取并逐表复核（Table 1 p.6、Table 2 p.9、Table 11 p.29、式 1 p.5、B.4.1 p.16、Figure 1 p.2）；建议人工抽查 Table 11 两三格与 PDF 原表对照。
