# opt-44 Pinterest的视觉搜索增长

- 文件：`07_垂直多模态_Pinterest_GEO_VLM_Agent_Framework.html`（arXiv 2602.02961v1，优化后 104,378 bytes）
- 审计发现：
  1. 23 处 `b-key` 出处全部错标「摘要与研究目标 · PDF p.1」；23 页 `.notes` 全是同一句模板腔。
  2. 无论文专属交互：改动实验室（p11）只有「操作前/操作后」两张示意文字卡，大片留白；教学示意（「桌子和椅子」）与论文真实例子（a woman in a pink dress → garden party outfit ideas）脱节。
  3. 证据读数页（p12）只有 3 个大数字卡加一张 Table 1 节选，无可比较图表；论文 7 张结果表（Table 2–8）一个都没用上。
  4. 自测 5 题模板腔，干扰项荒诞（「作者是否知名」「网页颜色是否好看」）。
  5. `finding_details` 每条约 28–30 字；发现页右栏无可视化、无论文数字。
  6. 专业层无公式：式 1 retain 门槛、式 2 SFT 损失、margin loss（m=0.95）、Table 2–8 全部缺席；指标页只有「先核对分母」泛话。
  7. 案例页未收录论文原例（`originalCases` 无 id 44）；论文内部口径不一致（摘要「数十亿图片」vs 结论「数亿图片」）未披露。
- 已做优化：
  1. 招牌交互（p11 改动实验室）：「从一张图到搜索入口的反推实验台」——左侧三步步进器走「用户问题 → 视觉表示 → 搜索入口」反推链路（① 反推 5–7 条查询：30/30/40 配比与式 1 三门槛（展示 >1000，或展示 >10 且 CTR ≥ 0.8，或排名 ≤ 10）、每图前 30 条；② embedding 聚合集合页：PinCLIP 0.881 对 SearchSAGE 0.848；③ VASE 双塔注解 + 内链）；右侧「注解策略切换」在无注解消融 / ANN 基线 / VLM 反推三档间切换，两组带 1.0× 基线竖线的条形图实时高亮对应行：用户会话 0.82×/1.00×/1.18×（Table 6）、生成式搜索流量 0.04×/1.00×/9.20×（Table 7），读数框随策略更新。专业层逐步补式 1、式 2、双 softmax、MLP [512,384,256]→128 维、margin 0.95、正确排名 0.981。步进器/策略按钮支持 aria-pressed、aria-live 与组内方向键（preventDefault）。
  2. 证据读数页（p12）重写为六标签页：生产结果（20% / 19% / 94× / 9.2× 四卡带出处）、流量消融（Table 6+7 双条形图、1.0× 基线竖线）、人工评估（Table 4 成对条形，5 分制：4.47/3.28、3.43/3.54、4.15/2.21，注 5 条 vs 9 条查询）、语义评估（Table 3 五维成对条形 %：96.15/97.70 等，注 GPT-4o 自评偏差 Δ −1.18 至 −2.34）、集合页 A/B（Table 5 四组成对条形）、原文表格（Table 1 节选 + 解读）。`PAPER.stats` 扩为 7 条全部带 `source`/`page`。
  3. 案例页（p18）改用论文原例：粉裙照片的图注与查询对比（Introduction p.2）+ 式 1 筛选门槛（§3.1.1 p.4）+ 三类查询真实例句卡（Soft Green Knit Dress / Sage Green Monochrome Look / Capsule Wardrobe Must-Haves 2026，§3.1.1 p.4），标注「未补造提升幅度」。
  4. 自测 5 题全部重写：核心结论（20% 与 94× 的口径）、反常发现（PinCLIP 离线赢、SearchSAGE 线上赢）、指标理解（Table 6 三倍数含义，干扰项混入 Table 7）、适用边界（整套部署 + 同口径复测）、局限（GPT-4o 自评偏差）；每题解释给复习页码。
  5. 发现页：4 条 `finding_details` 扩写至 88–92 字（含机制与论文数字）；每页右栏新增论文专属迷你图——F1 三类查询 30/30/40 条形、F2 Agent 四工具链（fetch_trends → semantic_filter → content_lookup → expand_query）、F3 离线意图满足率成对条形、F4 生成式流量三倍数条形，全部带出处。
  6. 指标页（p7）三指标各配论文口径与数字（+20%、4.47 对 3.28 p<0.01、低 94× + Table 8 参与度）；流水线页（p5）专业层按步给式 1/双 softmax+HNSW/margin 0.95；方法页步骤说明全部改为带数字的机制句。问题场景（p3）改用论文粉裙原例。
  7. `PAPER.limitations` 重写 6 条（整体归因、口径区分、评估偏差、摘要与结论「数十亿/数亿」不一致披露、41 号课对照、版本复核）；对照页、角色清单（控制台取数 / LoRA 微调 / 复现 0.881 差距等）、成熟形态（控制台证据档案 / 集合页质量双报告 / 消融记录）全部论文具体化。
  8. 文案与排版：23 页 `.notes` 全部重写为本页讲法；23 处 `b-key` 改为断言句 + 正确出处（Introduction p.2、§3.1–3.3 p.4–7、Table 4–7 p.7–9 等）；5 个泛化/疑问式 `b-title` 改为断言句（p3/p4/p5/p10/p11）；无「不是…而是」、无禁用词、无 emoji，数字与中文间半角空格。新增 CSS/JS 全部 `x-` 前缀（x-labgrid/x-labdoc/x-bars/x-brow/x-btrack/x-bfill/x-btick/x-bval/x-bcap/x-sw/x-tools/x-tool/x-arr/x-qcat/x-qc 及 xRow/xNumBody/xMetricHtml/xLabHtml/xFindViz/xCases/xPipePro）。PGS core 两段与外壳结构未动；23 页页数、`data-ch`/`data-t`/`data-view` 与 `.notes` 结构不变。
- 验收：`verify_one.py` 输出 `"pages": 23, "chapters": 7, "plain_overflow": [], "pro_overflow": [], "missing_notes": [], "quiz_complete": true, "interaction_overflow": [], "mobile_overflow": [], "mobile_plain_overflow": [], "errors": [], "broken_links": [], "pass": true`，bytes 104,378 < 200KB。两种模式 `PGS.checkAll()` 均为空数组；读数页 6 个标签、实验台 3 步 × 3 策略、组内方向键、自测 5 题流程逐一点击复检无溢出、无报错。
- 遗留：Table 8 各项参与度提升（+0.83% 至 +1.83%）仅在指标页专业层列示，未单独作图（页面空间所限）；「数十亿 vs 数亿」的规模表述以论文原文两处照录，已在局限页与批判阅读页说明以引用处原文为准。
