# opt-18 完整链路的SAGEO

- 文件：`03_GEO测量评估_SAGEO_Arena_Realistic_Environment.html`（85,945 B → 103,534 B，上限 200 KB）
- 论文：SAGEO Arena: A Realistic Environment for Evaluating Search-Augmented Generative Engine Optimization（arXiv:2602.12187v1，2026-02；实证测量。170K 网页语料 + 完整检索→重排→生成流水线的 SAGEO 分阶段评测环境；核心反直觉发现：仅改正文的改写会损伤检索与重排）

## 审计发现（Playwright 1440×900 无头 Chromium，优化前截图 23 页至 /tmp/opt-18/，两种模式 PGS.checkAll()；verify 基线本就全过——空壳无溢出）

1. 空壳模板：23 页全由通用 runtime 渲染，无任何论文专属交互；第 11 页「改动实验室」只有「操作前/操作后」两句模板抽象文案，页面大半空白。
2. 论文数据完全缺席：`PAPER.stats` 为空数组，封面右栏显示「本篇未在封面展示未经逐项核对的效果数值」；证据读数页跌入 numberless 兜底，全文没有 Table 2（十策略 × 三范围 × 三阶段）与 Table 3（StageAware 对比）的任何一个数字，而 Table 2 正是本篇的全部证据核心。
3. 反直觉发现零展开：摘要即点明的「改写损伤检索与重排」在课程里只有一句 claim，无机制（BM25 词面错开）、无极端案例（AutoGEO 检索名次 −22.35）、无 5.8% 第 10→11 名细节。
4. 自测五题全部模板腔（「哪项最准确概括本篇的核心贡献」式），答案就是 claim 原句；解释无出处、无数字。
5. `finding_details` 每条约 28 字且无数字；案例页 `originalCases` 无 id 18，只用 before/after 模板句——而论文 §5.1 有现成真实例子（eating→alimentary routines、Panel Clarifies Advice 标题改写）。
6. 23 页讲稿是同一句「这一页围绕……展开」；全部 b-key 出处一律误标「摘要与研究目标 · PDF p.1」（Table 2 在 p.6、式(4)(5) 在 p.5 等）。
7. 指标页无公式：H@k、ΔRank、RRF 融合（式 2-5）全部缺失，专业层只是重复通俗句。
8. 方法页/流程页的步骤说明是模板句拼接，未提 171,003 语料、BM25→Qwen3-Reranker-4B→gpt-5-mini 的真实配置。

## 已做优化

1. **签名交互（第 11 页「改动实验室」，标题改为「正文改得更专业，检索反而先丢分」）**：新增 `x-` 前缀分阶段影响演示——先选优化范围（仅改正文 / 仅改结构字段 / 两者都改），再沿「检索召回（BM25·top-100）→ 重排准入（交叉编码器·top-10）→ 生成引用（gpt-5-mini）」三关步进（节点按钮 + 上一关/下一关，组件内方向键 preventDefault）；每关展示改写前后数字卡（基线 0.58/1.00/0.50 vs 十策略均值）与机制转述，专业层补论文数字与出处；仅改正文 × 检索关亮出红色警示「反直觉：正文改得更专业，检索先丢 9%」。九种「范围 × 阶段」组合各有机制、结论与 warn 标记；默认状态即有完整解读。数字全部取自 Table 2 · PDF p.6（正文例 eating→alimentary routines、标题例 IOM Panel Clarifies Vitamin D Guidance 亦出自 §5.1 · PDF p.6）。
2. **证据读数页（第 12 页）重写**：4 视图——①范围 × 阶段：9 根相对基线的红绿发散条（零点线，−9%/−16%/−6%·+22%/−17%/+2%·+15%/−25%/−5%），图注写明三个阶段的基线口径；②十条策略仅正文检索 H@20 横条图，虚线基线 0.58，十条全部低于基线（AutoGEO 0.37 最触目）；③StageAware 对比（Table 3）：四组两两组合 + StageAware 0.75（绿色高亮越过基线）；④Table 2 节选表（检索阶段三范围 × ΔRank）。
3. **PAPER 数据补全**：stats 填入 4 条带出处的封面数字（−9%、−22.35、+22%、5.8%）；evidence 增补第 4 段「实现与语料」原文节选（附录 C · PDF p.11：256 token 分块、等权索引、top-100→Qwen3-Reranker-4B→top-10→gpt-5-mini）；before/after 写实（跳过检索与重排 vs 重新入库重跑同一查询）；GLOSSARY 增 BM25、重排器、结构字段、Hit Rate/ΔRank 四条。
4. **案例页（第 18 页）**：`originalCases` 加入 id 18 论文原例（改写后正文更好，目标文档为何在检索里消失了？——eating/sleeping 词面替换，重跑后 H@20 均值 0.58→0.53、AutoGEO 0.37/−22.35），标题改「一个词面替换就足以让文档掉出候选」，出处 §5.1 / Table 2 · PDF p.6，注明未补造提升幅度。
5. **自测重写 5 题**：核心结论（仅正文三阶段走向）、反常发现（AutoGEO −22.35，干扰项含 +4.86——StageAware 的数字）、指标口径（重排基线 H@10=1.00 的原因）、方法边界（StageAware vs 全部叠加）、适用局限（生产口径复测）；每题解释带数字与复习页码（14/12/7/16/21），正确项位置分散。
6. **发现页**：4 条 `finding_details` 扩写至 70–90 字并嵌入实测数字（0.58→0.53、−22.35、+22%/+2.72、5.8%）；每页新增 only-pro 证据条（F1 配 Table 1 旧基准对照，F2–F4 配 Table 2/3 关键行列）。
7. **专业层加深**：指标页 right 栏新增式(3)(4)(5) 公式（H@k、ΔRank）与 RRF 融合（式 2）说明，注明 k=100/10、缺失记 k+1；方法页三步各配论文配置（语料/流水线/对照口径）；证据读数页补口径注释（生成列百分比相对 0.50 计算等）。
8. **文案与讲稿巡检**：23 页讲稿全部重写为真实讲稿；23 个 b-key 全部改为带正确出处的断言句（Table 1/2/3、式(3)(4)(5)、§3.1/3.3/3.4/5.1、附录 C，本课推断类标注「本课编写」）；4 个弱断言页题升级（系统流程/方法拆解/改动实验室/案例拆解）；修正「重排一行全为负」为「重排在三种范围全为负」；数字与中文间半角空格核查；全文检索 `不是…而是 / 并非…而是 / 不只是…而是`、禁用词、emoji 均无；无 eval、无新增外部请求、无渐变。
9. **约束核对**：PGS core 两段与未动过的姊妹课程逐字节一致（脚本 diff 验证）；外壳骨架未动；23 页 `data-ch/data-t/data-view` 与 `.notes` 存在性不变，quiz 5 题 answer/nextQuiz/resetQuiz 流程不变；新 CSS/JS 类名全部 `x-` 前缀（x-pipe/xnode/x-nums/x-num/x-bars/x-brow/xbar/x-zero/x-dash 等）；新交互全部 `<button>` + `aria-pressed`，动态区 `aria-live="polite"`；方向键处理扩展到 x-pipe 且 preventDefault。

## 验收（verify_one.py 最终输出）

```json
{"pages": 23, "chapters": 7, "plain_overflow": [], "pro_overflow": [],
 "missing_notes": [], "quiz_complete": true, "interaction_overflow": [],
 "mobile_overflow": [], "mobile_plain_overflow": [], "errors": [],
 "broken_links": [], "bytes": 103534, "pass": true}
```

优化过程中修复的两处专业层溢出：指标页公式块移至右栏并合并说明（原左栏 +21px）、证据读数页口径注释压缩（原 +7px）。

## 遗留

- 无阻塞项。两点供人工复核：① 生成列百分比（+2%/−6%/−5% 等）按 Table 2 印刷值转录，未逐格重算相对基线；② StageAware 提示词全文（Table 5 · PDF p.12）未搬入课程，需要时可加到方法页专业层。
