# opt-4 网页搜索与生成回答

- 文件：`01_GEO基础框架_Navigating_the_Shift_Web_Search_vs_Generative_AI_Response.html`（arXiv 2601.16858v1，95,115 bytes）
- 审计发现：
  1. `PAPER.stats` 为空：封面右侧是占位卡，证据读数页只有「研究支持/尚需验证」两个空按钮 + 约 1,100 字符英文摘要倾倒，全课没有一个论文数字。
  2. 无论文专属交互：改动实验室只有「操作前/后」两张泛泛文字卡，大片空白；问题场景页为模板 before/after。
  3. 自测 5 题全是模板腔，干扰项与论文内容无关（如「保证所有引擎采用同一套来源」）。
  4. 案例页落模板兜底；论文本身有真实定性案例（SUV 查询漏引日志分析 + Table 3）未用。
  5. 23 页 `.notes` 全是同一句模板；`b-key` 出处全部错标「摘要与研究目标 · PDF p.1」。
  6. 发现页无任何可视化，正文重复标题，`finding_details` 单薄（约 25 字）。
  7. 专业层无公式无表格：Jaccard、Δavg、Kendall τ 与 Tables 1/2/3 均未呈现；evidence[1] 为乱码数学符号抽取，evidence[2] 与 evidence[0] 重复。
  8. metrics 仅 2 条且口径含糊，与论文实际测量（重叠/类型/年龄/漏引率）不对应。
- 已做优化：
  1. 招牌交互（p3 问题场景）：「同一查询，两条信息生态」双栏对照——左 Google 前 10 示意列表、右生成回答（引用角标），共有域名黄色高亮；下方 4 个引擎切换（GPT-4o 4.0% / Gemini 11.1% / Claude 12.6% / Perplexity 15.2%，Figure 1 实测），联动重叠量条与解读；支持方向键与 aria-pressed/aria-live。
  2. 改动实验室（p11）重写为论文 Table 1/2 扰动实验：三种扰动切换（SS/严格接地/ESI），热门 vs 小众 Δavg 双条形（基线 0），附 Kendall τ 一致性行与逐扰动解读。
  3. 证据读数（p12）重写为四维度切换条形图：域名重叠、来源类型（堆叠条，Google 为基线行，缺项注明减算口径）、文章年龄（Google 深色基线）、引用缺失率；专业层附 Table 1/2 原表与 Δavg、Jaccard 公式。
  4. 案例页（p18）改用论文原例：SUV 查询日志分析，16% 缺片段支持 + Table 3 六品牌漏引率条形图（本田 3% → 英菲尼迪 73%）。
  5. 发现页：4 条 `finding_details` 扩写至 55–95 字（补机制与数字），每页新增对应迷你图表（重叠/类型/年龄/Δavg），出处标签按 Figure 1、§2.2、§2.3、Tables 1–2 分列。
  6. 自测 5 题全部重写：核心结论（重叠区间）、反常发现（小众更敏感）、指标理解（Jaccard）、适用边界（口径做法）、局限（快照 + 单模型）；每题解释含复习页码。
  7. 指标页扩为 3 个指标（来源多样性/类型构成/新鲜度），专业层各配公式（Jaccard、构成和式、年龄中位数）与口径说明；方法页专业层补三种扰动定义与 Δavg 算式。
  8. 全部 23 页 `.notes` 重写为本页具体讲法；23 处 `b-key` 更正为带正确出处的断言；4 个含糊 b-title 改为断言句（问题场景/系统流程/方法拆解/改动实验室）。
  9. 封面右栏改为 4 个带出处的真实数据卡；金句页重写 6 条论文专属翻面卡；局限 6 条、复验清单、角色清单、成熟形态对照全部改为论文具体内容；evidence 三段重抽干净并标注正确页码。
  10. 新增 CSS/JS 一律 `x-` 前缀（x-duo/x-panel/x-serp/x-bar-row/x-track/x-fill/x-s1–3 等）；无 emoji、无禁用词、无「不是…而是」句式；PGS core 两段与外壳经 diff 确认逐字未动；页数/`data-ch`/`data-t`/`data-view`/`.notes` 结构不变。
- 验收：`verify_one.py` 输出 `"pages": 23, "chapters": 7, "plain_overflow": [], "pro_overflow": [], "missing_notes": [], "quiz_complete": true, "interaction_overflow": [], "mobile_overflow": [], "mobile_plain_overflow": [], "errors": [], "broken_links": [], "pass": true`，bytes 95,115 < 200KB。两种模式 `PGS.checkAll()` 均为空数组；交互后逐页点击复检无溢出。
- 遗留：Figure 3/4 论文只给分布图，正文仅报告中位数；课程按正文数值呈现并已在局限页注明「未逐图重算，以表格数值为准」。Gemini 社交占比（8%）与 Perplexity 社交占比（11%）为 100% 减算，已在图注标明。
