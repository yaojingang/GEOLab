# opt-61 考虑竞争的策略组合
- 文件：`02_GEO方法优化_Beyond_the_Vacuum_Competitor_Aware_GEO.html`
- 论文：Beyond the Vacuum: Combinatorial Strategy Selection for Competitor-Aware GEO · arXiv:2608.27631v1 · 实证方法
- 审计日期：2026-11-05（Playwright 无头 Chromium，1440×900 截图 23 页至 /tmp/opt-61/，通俗+专业两种模式各跑一次 PGS.checkAll()；论文全文用 pdftotext -layout 抽取并逐页定位表格）

## 审计发现
1. `PAPER.stats` 为空：封面右侧是"本篇未在封面展示数值"占位卡，证据读数页（p12）落入 numberless 兜底，全课没有一个论文实测数字；Table 1/2/4/5 与 Figure 2 的关键读数（32.62 / 29.93 / 11.4% / 84% / 17.99）完全未使用。
2. 无论文专属交互：改动实验室（p11）只有"操作前/后"两条模板句（"沿用单篇离线测试的最优方案"），大面积留白，与论文核心机制（对手画像决定最优组合）无关。
3. 案例页（p18）用兜底示意，而论文附录 K 有真实案例（Table 12/13：两个查询在 α=0.0/0.4/0.8 下推荐组合与推理摘录，含"平衡观点先加后撤"弧线），`originalCases` 未收录 id 61。
4. 自测 5 题为模板腔，干扰项与本篇无关（"网页颜色是否好看"等），未覆盖反常发现（无改写基线跌至 17.99；Table 3 忠实度 4.90 低于不改写 8.29）。
5. `finding_details` 四条约 27–30 字（<40 字下限）；发现页出处全部笼统标"摘要与研究目标 · PDF p.1"，且无逐条专业层。
6. 专业层浅：无 PAWC 公式（式 3）、无 BOCS 代理模型（121 项二阶多项式）、无偏好对阈值 t=1.860、无 Table 5 消融。
7. 文案错位：`PAPER.table` 是版面乱抽（Table 1 与正文混排、列错位）；23 页 b-key 全部同一出处；23 页 .notes 全部同一段模板话术；指标名"印象指标"未落到 PAWC；"C-SEO Bench发现""本地PDF"缺半角空格。

## 已做优化
1. **招牌交互（p11 改动实验室）**：重做为"对手压力模拟器"——围绕「不同对手画像 → 最优策略组合」，两个真实查询 tab（what is a kin / australian dollar currency converter，query_id 450/972）× 三档竞争压力（α=0.0/0.4/0.8）切换；左栏显示"对手在做什么 + 选择器推理摘录（中文摘译）+ 推荐组合 chips（相对上一档：新增绿色标 +，撤下红色删除线）"，右栏为读法解释、选择器信息集说明（只看查询与语料，看不到 α 与分数）与实测锚点（29.93 对 25.20/17.99，Table 2）。数据全部转述自附录 K · Table 12–13（PDF p.20），逐处标注出处与"论文原文节选的转述"。按钮 `aria-pressed`，动态区 `aria-live="polite"`，复用课程现有方向键委托（choice-row）。
2. **证据读数页（p12）**：`PAPER.stats` 填入四组实测数（32.62 原始语料 / 29.93 竞争语料 / 11.4% 全程降幅 / +3.35 有据推理增益，各带 context 与 Table 1·2·Figure 2·Table 5 出处页码）；大数字卡 + 五条带基线横条图（虚线基线 = 无改写 20.03，HTML/CSS 绘制）+ 保留"原文表格节选"（`PAPER.table` 换成干净的 Table 2 六行抽取）；专业层新增 Table 5 关键行（21.53/23.92/32.62/39.00 + 完整梯度文字）；加"去改动实验室"跳转联动。
3. **封面数字卡**：stats 驱动后自动变为四个实测数字瓦片（32.62 / 29.93 / 11.4% / +3.35，各带出处）。
4. **案例页（p18）**：`originalCases[61]` 收录附录 K 论文原例（中文转述：澳元转换查询，α=0.4 加平衡观点、α=0.8 因对手饱和而撤下），标题改"平衡观点先加后撤：一次真实的组合调整"，出处 Table 13 · PDF p.20。
5. **自测 5 题重写**：覆盖两段流水线（方法）、无改写基线跌至 17.99 的含义（反常）、PAWC 位置衰减原理（指标）、合成竞争边界（适用边界）、Table 3 忠实度代价（局限）；每题解释含出处与复习页码（p10/p14/p7/p21/p21）。
6. **发现页（p13–16）**：`finding_details` 扩到 55–78 字并补机制证据；逐条真实出处（Table 1 vs 2 / Figure 2 / Table 5 / Table 4）；每条新增 `.only-pro` 专业层（两环境单策略对照、α 口径与 11.4%、偏好对构造参数与 0.93% 泄漏审计、零样本换算与合成竞争未测项）。
7. **专业层加深**：指标页（p7）补 PAWC 公式（式 3）与 Pos Count/Word Count 关系；方法页（p10）补 BOCS 代理模型公式（121 项、horseshoe、模拟退火、50 次评估）与 Algorithm 1（Welch t 阈值 1.860、Hamming 最近负例）；证据读数页补 Table 5 消融表。
8. **数据与术语**：metrics 改为 PAWC / 组合收益（含通俗口径）；steps、query/before/after 对齐论文（对手语料 → BOCS 搜索 → 偏好对微调）；GLOSSARY 增补 BOCS / DPO / 采用率 α / 偏好对 / 硬负例；limitation 第 2、3 条改为论文自述的代理评估与 15 策略非穷尽。
9. **文案与排版巡检**：23 页 b-key 全部换成真实出处（Table 1–2 · PDF p.5,7 等）；23 页讲稿（.notes）逐页重写；7 个页面标题改为更具体的断言句；修复"C-SEO Bench发现""本地PDF"缺空格；全文 grep 无"不是…而是"句式、无禁用词、无 emoji。
10. **无障碍与约束**：新组件全部 `x-` 前缀（x-lab / x-qtab / x-comp / x-quote / x-chips / x-chip / x-bar-row / x-bar-track / x-bar-fill / x-maxline），移动端单栏适配；未动 PGS core、外壳、页数、data-ch/data-t/data-view 与 quiz 动作名；未引入外部请求与 eval；`innerHTML` 只拼接常量与 esc 后的 PAPER 字段。

## 验收
`verify_one.py 02_GEO方法优化_Beyond_the_Vacuum_Competitor_Aware_GEO.html` 最终输出（JSON 摘录）：
```
pages=23, chapters=7, bytes=98055
plain_overflow=[], pro_overflow=[], interaction_overflow=[],
mobile_overflow=[], mobile_plain_overflow=[], missing_notes=[],
errors=[], broken_links=[], quiz_complete=true, pass=true
```
调试过程中修复：p12 通俗/专业双溢出（数字卡改 44px、Table 5 缩为关键行、图注合并、去重复口径提示）；p13/15/16 专业层 8px 溢出（间距收紧）；375px 移动端抽查 p11/p12/p14 无横向滚动；两种模式 PGS.checkAll() 均为空数组；控制台零报错。

## 遗留
- 论文三个对手改写函数 W1/W2/W3（随机组合/最强单策略/AutoGEO）在课程中仅以"对手在做什么"一行转述，未展开各自 PAWC（论文未按 W 分列报告结果）。
- Figure 2 各 α 点的具体 PAWC 数值论文未在正文/表格给出，课程只引用其文字结论（11.4%、α=0→0.2 无显著下降、单策略 α=0.8 跌破基线），未绘制逐点曲线。
- 对手压力模拟器的推理摘录为中文摘译（标注"转述"），措辞与原文逐字对照建议人工复核一遍（Table 12/13 · PDF p.20）。
- Table 6（代理阶数 +0.39）与 Table 7 全表未展示，仅在发现 3 专业层引用泄漏率 0.93%。
