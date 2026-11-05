# opt-87 枢纽与权威相互强化（Kleinberg HITS）

- 文件：`13_链接分析与外链理论_C05_Authoritative_Sources_in_a_Hyperlinked_Environment.html`
- 论文：Authoritative Sources in a Hyperlinked Environment（SODA 1998 / JACM 1999，本地 PDF 逐节核对）
- 日期：2026-11-05 · 执行：单篇互动课优化任务（spec v1）

## 审计发现（优化前）

1. 全课无论文专属交互：HITS 的「I/O 交替更新、互强化收敛」机制没有任何可视化，与 PageRank 的差异完全没讲。
2. 发现页内容错位（严重 bug）：发现 4「主题过窄时扩散」的详情显示的是 Clever 用户研究数据，`finding_details` 相对 `findings` 错位一位。
3. 出处千篇一律：23 页 `.src` 全部是「摘要与研究目标 · PDF p.1」，stats 的 page 字段也全是 1，无法核验。
4. 概念页（p4）用流程步骤冒充概念，权威/枢纽/互强化挤在侧栏小字；指标页（p7）半空，专业层无任何公式。
5. 证据读数页只有大数字卡：50/31/19、java 权威分等可比数值没有条形图；「原文表格节选」按钮指向 `table: null`，点击只提示「未找到」。
6. 改动实验室与案例页用抽象教学示意，论文真实案例（search engines 查询、Gates 榜首 roadahead.com 仅列第 123、java 入度混入度假广告页与 Amazon）全部缺席。
7. 自测 5 题是模板题：第 1 题正确项是 77 字长句；`.notes` 23 页全是同一句模板话；BibTeX `year` 字段为「期刊）」（生成 bug）；`PAPER.evidence` 第 3 条与第 1 条重复。

## 已做优化

1. **招牌交互「HITS 迭代演示」（p10 方法拆解）**：8 节点小图（3 枢纽、3 权威、1 泛流行页 X、2 导航页），每次点击执行半步——I 操作（用枢纽分更新权威分）与 O 操作（用权威分更新枢纽分）严格交替并 L2 归一化，忠实对应论文 §3 的 Iterate 伪代码。节点旁实时显示分数，双列条形图同步，相位条显示「已完成半步数 / 最大变化 / 下一步操作」，动态讲评随迭代推进（X 第 1 轮与权威并列→逐轮萎缩→归零，A3 与 X 同为 2 条入链却因入链者是好枢纽而保分）。收敛值与 AᵀA/AAᵀ 主特征向量解析解一致（A1=A2=0.628、A3=0.460、X→0；H2=0.789）。控件为 `<button>`，置于 `.choice-row` 内支持方向键（复用 core 的 preventDefault 捕获处理），动态区 `aria-live="polite"`。图下注明「教学示意，节点与边为本课构造」。同页右下给「与 PageRank 的三点差异」（传递路径 / 计算时机 / 结果形态，§5 · p.17）。
2. **证据读数页重写（p12）**：6 块读数——1369 大数字卡+口径、50/31/19 战绩横条图（37 名用户盲评 · §8 p.26）、39800 根集稀疏度（15/28 条按线性比例的细条，图注说明「细到几乎不可见正是无结构的含义」）、java 权威分条形图（.328-.183 论文实测 · §3 p.11）、20 轮收敛（附跳转演示按钮）、原文结果表节选（`PAPER.table` 补上 java / search engines / Gates 三组真实权威分表）。
3. **案例页换成论文原例（p18）**：`originalCases[87]` 写入 search engines 查询案例（五家引擎首页不含查询词；Gates 例 roadahead.com AltaVista 第 123；操作与检查含 0.346-0.231 权威分），出处 §1 p.2 + §3 p.11-12。
4. **改动实验室重写（p11）**：操作前=论文 §3 p.7 原文列举的 java 入度最高页面构成（gamelan、java.sun.com 与度假广告页、Amazon，红标坏答案）；操作后=HITS 前 5 权威及分数（§3 p.11）；并排比较给出「差别来源」解释。
5. **自测 5 题全部重写（p23）**：覆盖循环定义如何打破（机制）、search engines 为何文本找不到（反常发现）、权威分更新规则（指标理解）、适用查询类型（边界）、Clever 研究读法（评估口径）；干扰项貌似合理，每题解释给复习页码（10/13/7/6/12）。
6. **发现页修正与加深（p13-16）**：修复 finding_details 错位，四条详情按论文重写（Harvard/search engines · java 入度混入 · jaguar 三义与 abortion 正负端 · WWW conferences 扩散与第 11 非主向量补救），每条带节号与页码；新增 `finding_src`/`finding_check`（每条发现配专属核查项，替换错误的指标轮换映射）。
7. **专业层加深**：指标页（p7）给出 I/O 更新式与 AᵀA/AAᵀ 主特征向量（定理 3.2 · p.10-11）、PageRank 转移公式 A′ᵢⱼ（§5 · p.17）；概念页 pro 层给矩阵记法；实验设计页换成 4 段不重复的原文节选（摘要 / §2 构图 / §3 迭代定理 / §8 Clever）。
8. **全课文案巡检**：23 页 `.b-key` 全部改为本页断言+真实出处；23 页 `.notes` 重写为真实讲稿；PAPER.stats 页码修正（26/26/5/11）；`limitations` 六条细化（Clever 叠加锚文本启发式、m≈4-8 未启用等）；persona「避免」句修通；mature 形态换为本课专属三形态；quotes 六卡背面写具体依据与用法；对照页补 PageRank 对照；BibTeX year 修为 1999；无禁用句式/禁用词/emoji（已扫描）；文件 103.9 KB。
9. **数据层与表现层分离**：论文数字全部落在 `PAPER` 对象（stats/table/lab/quotes/finding_src/finding_check/evidence），渲染函数只读数据。

## 验收

`python3 _build/verify_one.py 13_链接分析与外链理论_C05_….html`：

```json
{"pages": 23, "chapters": 7, "plain_overflow": [], "pro_overflow": [],
 "missing_notes": [], "interaction_overflow": [], "mobile_overflow": [],
 "mobile_plain_overflow": [], "quiz_complete": true, "errors": [],
 "broken_links": [], "bytes": 103853, "pass": true}
```

另核对：HITS 演示数学与解析解一致（幂迭代 13 半步后 X=0.003→显示 0.00）；1440×900 通俗/专业双模式 `PGS.checkAll()` 均空；23 页逐页截图复核通过。

## 遗留

- 无阻断项。备注两条供人工复核：① 论文未给「操作前」入度排序的具体分值，p11 左栏按原文列举转述并已标注；② 演示小图数值为示意构造的迭代结果（与论文机制一致），页面已标注「教学示意」。
