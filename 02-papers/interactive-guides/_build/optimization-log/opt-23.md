# opt-23 AI摘要怎样改变搜索

- 文件：`04_AI搜索实证_How_Generative_AI_Disrupts_Search_Google_AI_Overviews.html`（102,434 bytes）
- 论文：How Generative AI Disrupts Search: An Empirical Study of Google Search, Gemini, and AI Overviews（SIGIR '26，本地 PDF SHA-256 e13a5a0e…）

## 审计发现

1. 全部 23 页均为模板渲染：页面内容只拼 `PAPER` 通用字段，正文几乎不含论文数字，讲稿 23 页完全同文（「这一页围绕……展开」）。
2. 除封面 4 个数字卡（11,500 / 14,212 / 51.5% / <0.2）外，论文核心数值全部缺席：65.6%、ELI5 94.6% vs Amazon Retail 17.4%、NQ 86.2% vs NQ Keywords 76.5%、问句 89.9% vs 非问句 51.9%、Table 2 重合度、Table 4 一致性、Figure 4 热门域名占比、立场 33.4%/5.6% 等。
3. 第 11 页「改动实验室」近乎空页：仅两个含糊文本卡（操作前/后），无数据无交互密度。
4. 第 12 页「证据读数」只有大数字卡，无可比条形图与基线；「原文表格节选」落到「未找到表格」兜底（`PAPER.table=null`）。
5. 第 13–16 页发现页无任何可视化，`finding_details` 均不足 40 字，四页右栏内容重复。
6. 第 18 页案例页用教学填充问题，未使用论文真实定性案例（§4.5 Figure 8 拳赛误信息 AIO）。
7. 第 23 页自测为模板题：答案与 `PAPER.claim` 原文相同、含玩笑干扰项（「网页颜色是否好看」）、解释不给复习内容。
8. 专业层几乎为空：无 Jaccard/RBO 定义、无 Table 2/4 关键行列、无采集口径（SerpAPI 移动端、2025-12-07/08、RBO p=0.9）；各页 `b-key` 出处一律误标「摘要与研究目标 · PDF p.1」。

## 已做优化

1. **招牌交互（p11 改动实验室）**：新增「查询触发实验室」两步演示。第一步在论文 Table 1 的 8 条真实基准查询（ELI5/商品问句/商品比较/NQ/同题关键词版/ORCAS/本地服务/商品关键词）间切换，显示该子集实测触发率（94.6%→17.4%）与问句/非问句、商品问句/关键词对照条；第二步显示触发后来源变化：该子集 AIO×SERP 的 Jaccard（0.08–0.21，基线 0.18）与三引擎 Top-1K 热门域名占比卡（SERP 37.8%、AIO 36.5%、Gemini 27.9%）+ Google-Extended 屏蔽反常点。全部按钮 `<button>` + `aria-pressed`，输出区 `aria-live="polite"`，方向键沿用 choice-row 处理并 `preventDefault()`。
2. **证据读数页（p12）重写为四标签条形图**：触发率对比（10 个子集 + 政治人物 93.8%/趋势 8.1%，虚线基线 65.6%）、来源重合度（三对界面 Jaccard/RBO，0–1 轴 + 总样本均值虚线）、一致性对比（Table 4 同题两运行 + 200 条微改后 RBO）、原文表格节选（Table 2 摘录，`PAPER.table` 补齐）。纯 HTML/CSS 条形图，全部带出处 `.src`。
3. **发现页（p13–16）**：新增 `findingViz()` 每条发现配迷你条形图（引擎配色一致：SERP 蓝/AIO 绿/Gemini 橙），`finding_details` 扩写到 60–90 字并补机制证据，实践含义/适用条件改为逐条定制（`fimplies`），专业层补 χ²、子集区间、设备/文本相关性等。
4. **案例页（p18）**：录入论文原例 `originalCases[23]`——趋势查询 “who won jake paul or anthony joshua” 在比赛当晚被 AIO 抢先宣布胜者、引用中仅一条讽刺 Facebook 帖子支持（§4.5/Figure 8），配 33.4% vs 5.6% 立场卡与 F1/F4 关联说明；明确「论文未给数值，不估造收益」。
5. **自测（p23）重写五题**：核心数字（ORCAS 51.5% 分层）、反常发现（屏蔽 Google-Extended 反而少被 AIO 引用）、指标理解（Jaccard 口径）、适用边界（关键词 17.4% vs 问句 92% 的阶段含义）、研究局限（Google 系/单一时点/API 采集）；每题解释带数字与复习页码（13/15/14/13/21）。
6. **专业层加深**：指标页增至 3 个指标（触发率/Jaccard/RBO），各带 `.formula` 定义式与口径 pro-note（p=0.9、URL 级、分母差异）；p12/p13–16 pro-note 补 χ² 检验、平均来源数、设备与文本相关性、Table 3 结论。
7. **数据层与文案**：`PAPER` 重写（steps/finding_details/evidence[2] 改为 RQ1 原文、stats 出处精确到 Table 1 p.3 等）；p19 角色行动、p20 成熟形态、p22 金句全部改为论文专属内容；23 页 `b-key` 与 `.notes` 逐页重写并标注正确出处（Table/Figure/§ · PDF 页码）；p3 增加据 Figure 1 的结果页结构示意（标注示意）；p21 局限六条改为论文具体边界（Google 系、单一时点、SerpAPI 差距、MBFC 覆盖率等）。
8. **文案巡检**：全文 0 处「不是/而是」句式、0 禁用词、无 emoji（☰/✓ 为外壳符号）；新增 CSS/JS 均 `x-` 前缀；术语表新增 AIO/Google-Extended/Tranco/立场性回答。
9. **约束遵守**：PGS core 两段与外壳结构未动；23 页 `data-ch/data-t/data-view` 与 quiz 动作名保持；无外部请求、无 eval、`innerHTML` 仅拼接常量与 `esc()`。

## 验收

`python3 _build/verify_one.py 04_AI搜索实证_How_Generative_AI_Disrupts_Search_Google_AI_Overviews.html`

```json
{"pages": 23, "chapters": 7, "plain_overflow": [], "pro_overflow": [],
 "missing_notes": [], "quiz_complete": true,
 "interaction_overflow": [], "mobile_overflow": [], "mobile_plain_overflow": [],
 "errors": [], "broken_links": [], "bytes": 102434, "pass": true}
```

另自检：1440×900 通俗/专业两模式 `PGS.checkAll()` 均为 `[]`，控制台零报错；优化前后截图存 `/tmp/opt-23/`。

## 遗留

- 数字均按本地 PDF（-layout 抽取）逐项核对；Figure 2b 信息/导航/事务意图的触发率仅见图未在正文给出，课程未引用具体数值。
- Figure 3/5/7 的逐域名数值未逐条搬入（版面抽取列对齐风险），课程只用其汇总结论并标注出处。
- 政治人物 93.8% 与趋势 8.1% 来自独立时点查询集（非 11,500 基准），课程内已区分标注；引用时请注意分母。
