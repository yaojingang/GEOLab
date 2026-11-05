# opt-35 商品描述影响推荐

- 文件：06_风险操纵_Manipulating_LLMs_to_Increase_Product_Visibility.html（96,972 bytes < 200 KB）
- 论文：Manipulating Large Language Models to Increase Product Visibility（Kumar & Lakkaraju，arXiv 2404.07981v2，风险研究）

## 审计发现（优化前）

1. 封面无关键数字，右侧卡片自述"本篇未在封面展示未经逐项核对的效果数值"——根因是 PAPER.stats 为空。
2. 证据读数页（p12）没有任何数字与图表，只有英文摘要节选；改动实验室（p11）仅两栏含糊示意文本（"将商品自述中的选择要求直接执行"），近乎空板。
3. 全部 23 页的本页要点出处一律是"摘要与研究目标 · PDF p.1"（错误标注）；讲稿全部为模板腔（"这一页围绕…展开。请先观察默认状态…"）。
4. 自测五题为模板题，正确答案直接复述 claim，无复习定位价值。
5. finding_details 每条仅 24–31 字，单薄。
6. PAPER.evidence 三段原文节选均在中途截断（"Code for our experi"、"even for products close to"、"potential mis"）。
7. 案例页有原例框架但无具体查询、注入文本与模型回答；角色页"避免：{before}后，直接宣称…"拼接语法不通。
8. 指标页专业层只重复通俗文本，无口径公式；问题场景页 mock 含糊且留白过多。

## 已做优化

1. **招牌交互「STS 实验台」（p11 改动实验室）**：目标商品（ColdBrew Master $199 / QuickBrew Express $89）× 注入文本（不加 STS / 固定顺序优化 / 随机排列鲁棒）两级开关；输出三联面板——模型看到的商品字段（注入文本高亮，转写自论文 Figure 3 · PDF p.5 示例；QuickBrew 论文未公布原文，标注示意）、200 次成对评估排名变化条形（更高/不变/更低：ColdBrew 固定 ≈38/61/1、鲁棒 ≈95/3/2，QuickBrew 固定 ≈16/65/18、鲁棒 ≈48/50/0，读自 Figure 5a/5b/7a/7b · PDF p.7/9，均标"读图约值"并注明成对基线）、识别信号与防御动作（字段尾部乱码、推荐与查询条件矛盾、消费者核对与平台侧隔离过滤）。全部 `<button>` + aria-pressed + aria-live，方向键在组内切换（preventDefault）。
2. **证据读数页（p12）重写**：按商品切换的分组条形图（HTML/CSS，自 0 起算，带数据标签与图例），右侧大数字卡（≈95% / ≈48%）+ 口径要点；封面同步获得 4 张带出处的数字卡（修复 stats 为空；并修复对象字面量中尾部重复 `"stats": []` 覆盖取值的问题）。
3. **案例页（p18）升级为论文原例**：真实查询、注入前后商品 JSON 字段对照（STS 乱码高亮）、模型回答矛盾点（$199 被称 relatively inexpensive，Response · PDF p.6）、识别信号，出处 Figure 3/Response 标注。
4. **自测五题重写**：核心结论（Figure 4b 前后分布）、反常发现（换序后固定 STS 优势与劣势相抵）、指标口径（优势的成对定义）、注入文本识别（乱码 token 干扰项）、研究边界（虚构目录限制外推）；每题解释含出处与复习页码。
5. **发现四条扩写至 75–90 字**并补证据出处；发现页新增专业层注记（Figure 4b/6b/5a/7a 与 §5 细节）。
6. **专业层加深**：指标页新增 3 条口径（名次解析规则、优势成对定义、GCG 交叉熵目标函数，§3/§4.1 出处）；实验设计页原文节选补全为四段完整摘录（摘要/方法目标函数/结果与评估/讨论边界）。
7. **文案巡检**：删除全部模板讲稿，23 页讲稿逐页重写（2–4 句口语化）；23 页本页要点逐页改写为断言式要点并配正确出处；修复角色页"避免"句拼接语病；steps/before/after 更新为具体表述；无"不是…而是"句式、无禁用词、无 emoji，数字与中文间加半角空格。
8. 金句页 6 卡重写为论文专属（结论/依据/用法三段），复制按钮同步。

## 验收

`python3 _build/verify_one.py 06_风险操纵_Manipulating_LLMs_to_Increase_Product_Visibility.html` →

```json
{"pages": 23, "chapters": 7, "plain_overflow": [], "pro_overflow": [],
 "missing_notes": [], "quiz_complete": true, "interaction_overflow": [],
 "mobile_overflow": [], "mobile_plain_overflow": [], "errors": [],
 "broken_links": [], "bytes": 96972, "pass": true}
```

## 遗留

- 条形图数值为从论文 Figure 5a/5b/7a/7b 读取的约值（图内无数据标签），已逐处标注"读图约值"并附文字口径（§4.1 "约 40%/约 60%"）；如需精确值需向作者要原始数据。
- Figure 4b/6b 的名次分布以文字口径转述（"几乎全部第一"），未作逐点计数，避免误读点图。
