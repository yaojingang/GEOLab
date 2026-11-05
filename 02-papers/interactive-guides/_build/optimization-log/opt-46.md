# opt-46 搜索与推理解耦

- 文件：`08_AI搜索架构与AgenticSearch_Decoupled_Search_Grounding_LLM_Agents.html`（arXiv 2606.18947v1，101,827 bytes）
- 审计发现：
  1. 无论文专属交互：改动实验室（p11）只有「操作前/后」两张泛泛文字卡，大片留白；全课没有用到论文最有价值的耦合 vs 解耦实测对比（Table 1/4/5）。
  2. 证据读数页（p12）只有大数字卡 + 口径卡，无可比条形图、无基线；pro 层对照条仅 2 条且不在通俗层出现。
  3. 案例页（p18）用 2 句教学示意占位；论文真实定性案例（Table 9 的 Gulangyu 精确匹配失败例、§3 的 200 West Street 245 字符对 3 字符例）未使用。
  4. 自测 5 题模板腔（干扰项如「网页颜色是否好看」）；`finding_details` 每条约 25 字且发现页无可视化。
  5. 23 页 `.notes` 全是同一句模板；23 处 `b-key` 出处全部错标「摘要与研究目标 · PDF p.1」。
  6. 专业层无论文公式（式 1 缓存门控决策）、无完整 Table 1；指标口径与论文不符（准确率未说明 GPT-4.1 评判 vs EM/F1，成本未说明不含推理费）；p5 pro 层有「？。」双标点拼接错误。
  7. 口径风险：99.4% 热缓存命中率是重复查询重放实验（Table 7），生产 QIU 缓存命中仅 1.15%–26.77%（Table 5），课程未区分，易被误读为生产值。
- 已做优化：
  1. 招牌交互（p11 改动实验室）：「架构对比台」——五个任务类型切换（SimpleQA 单跳 / FreshQA 时效 / HotpotQA 多跳 / QIU Retail 生产意图 / QIU Tail 长尾），每个任务下并排比较无搜索、原生搜索（耦合）与 DSG+BrightData、DSG+Serper（解耦）四个架构的准确率条（0–100%）与每千次搜索成本条（0–各任务最大值），数据全部来自论文 Table 1/4/5 实测；读数卡按任务给出论文结论（如 FreshQA 原生全模型领先、QIU Tail DSG+Serper 反超且降本超 98%）；专业层附 SimpleQA 的 95% 自助区间（原生 [86.82, 88.64] 与 DSG+BrightData [85.18, 87.06] 重叠，Table 6）。按钮用 `aria-pressed`、读数区 `aria-live="polite"`、方向键组内切换 `preventDefault()`。
  2. 证据读数（p12）重写：6 个读数（86.1% / 87.7% / 91% / 99.4% / 1,465 ms / 78.1%）各配「对照读数」零点起算横条对（蓝=DSG、橙=原生、灰=无搜索/冷路径）+ 尺度说明 + 出处；第 7 档为按 PDF 表值转写的 Table 1 完整节选；每条 context 写明口径（成本不含推理费、重放对生产命中率）。
  3. 案例页（p18）改用论文原例：Table 9 的 Gemini 2.5 Flash「Asante Traditional Buildings 与 Gulangyu 哪个大」——原生搜索输出解释文导致精确匹配失败，无搜索输出干净答案实体；并附 §3 的 200 West Street 例（245 字符对 3 字符），标注出处 Table 9 · PDF p.15 与「未补造收益幅度」。
  4. 自测 5 题全部重写：核心结论（FreshQA 原生全模型领先）、反常发现（Search-Induced Verbosity 定义与 78.1%/62.3% 数字）、指标理解（搜索成本=每千次提供方费用不含推理费）、适用边界（99.4% 是重放实验，生产 QIU 1.15%–26.77%）、局限（多跳增益有限）；每题解释含复习页码。
  5. 发现页 4 条 `finding_details` 扩写至 78–90 字并补机制数字；每页右栏新增论文专属迷你图（F1 五类控制 chips + 五模型可替换、F2 冷热路径命中/时延对照条 + 深度饱和注记、F3 FreshQA 四架构条形、F4 中位长度 353/13/13 条形 + 78.1% 注记），出处按 §4/Figure 4/Table 7/Table 1/Table 8 分列；「实践含义」改为论文专属推断文案。
  6. 专业层加深：系统流程页（p5）补论文式 1（精确缓存 → 语义缓存 τ 阈值 → 回退链）与 Algorithm 1 口径；指标页（p7）三指标各给完整口径（GPT-4.1 评判、3 评委一致率 97.78%、EM/F1、$/1K 不含推理费、中位数与 P95）；实验设计页（p8）加样本量标签（N=1,000/500/1,000/7,988/2,335）与评判口径 callout；方法页约束改为提供方隔离缓存键、按域 TTL、来源 URL（§4.1/§4.3/Table 10）；局限页 6 条全部替换为论文具体局限。
  7. 问题场景（p3）改为耦合 vs 解耦两种接法对照（对齐 §3 四个部署挑战）；角色清单、成熟形态、金句 6 张、对照检查、研究对照全部论文具体化（避免把重放命中率当生产收益等）。
  8. `PAPER.stats` 扩为 6 条带 `cmp` 对照数据；`PAPER.table` 换成按 PDF 表值转写的干净 Table 1；evidence[2] 换成输出契约诊断原例；23 处 `b-key` 更正出处；23 页 `.notes` 全部重写为本页具体讲法；修复 p5「？。」双标点。
  9. 全文清理：无「不是…而是」句式、无禁用词、无装饰 emoji；数字与中文间半角空格；新增 CSS/JS 一律 `x-` 前缀（x-prow/x-pl/x-ptrack/x-pfill/x-f0/f1/f2/x-pv/x-ncmp/x-btable/x-bline/x-bname/x-bcell/x-btrack/x-bval/x-blegend/x-case/x-cdoc/x-cq）；PGS core 两段与外壳结构未动；23 页页数、`data-ch`/`data-t`/`data-view` 与 `.notes` 结构不变。修复过程中发现并纠正了批量替换丢失 `.board` 闭合标签的问题（`.notes` 曾被移入白板内导致讲稿可见，已恢复）。
- 验收：`verify_one.py` 输出 `"pages": 23, "chapters": 7, "plain_overflow": [], "pro_overflow": [], "missing_notes": [], "quiz_complete": true, "interaction_overflow": [], "mobile_overflow": [], "mobile_plain_overflow": [], "errors": [], "broken_links": [], "pass": true`，bytes 101,827 < 200KB。两种模式 `PGS.checkAll()` 均为空数组；交互逐页点击复检（含架构对比台 5 任务切换）无溢出、无报错；375px 下 p11/p12 无横向滚动。
- 遗留：HotpotQA 对比台一行使用 Gemini 2.5 Flash 单模型 EM（Table 4，论文未报五模型均值），已在校准图注标注；QIU Retail 降本 98.6% 为按 Table 5 表值换算的派生数（论文只写 Tail「over 98%」），口径已在页内注明「按表值换算」。Table 2 中 Gemini 2.5 Pro 的 DSG+Serper 成本 50.86 疑似论文排版异常，课程未采用该行。
