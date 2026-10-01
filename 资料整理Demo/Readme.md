# 大二资料整理

## 项目简介

直接对英文课件（PPT / Word）进行归纳整理与讲解，迅速串联知识、建立知识体系。**不翻译**：直接阅读理解英文源文件，生成中文的细粒度讲解与粗粒度摘要。

- **输入**：若干英文课件文件（PPT / Word）。
- **当前阶段**：直接对英文源文件做知识点总结与讲解，并建立课程级知识体系。

## 架构

- `Readme.md`：项目唯一「无上下文入口」（规范见 `CLAUDE.md`）。
- `.claude/skills/`：讲解用 skills，均手动触发：
  - `summarize-knowledge/`：知识点总结与讲解（英文 Word/PPT → 细粒度详细讲解 + 粗粒度摘要两份 md，摘要内嵌锚点链接；含 `SKILL.md`（触发/输入/流程）+ `知识点讲解原则.md`（细粒度讲解规则）+ `知识点总结原则.md`（粗粒度摘要规则））。
  - `locate-knowledge/`：跨文件定位知识点（返回文件#锚点链接）。
  - `course-summary/`：课程级知识体系总结（汇总各课件摘要，展现跨课件知识点联系，附 Mermaid 图谱）。
  - `summary/`：一键编排（自动判断文件类型，严格按 讲解 → 总结 串行执行两个 skill）。
- `content/Raw/`：源文件（英文，按课程子目录存放，如 `content/Raw/GEC3407/`）。
- `content/Reflect/`：讲解产物（相同子目录结构，按文件建文件夹，含 `全文.txt`（英文原文抽取）/ `<文件名>-专有名词.md`（专有名词对照表）/ `<文件名>-知识点讲解.md` / `<文件名>-知识点摘要.md`；课程目录下另含课程级 `讲解原则.md` 与 `<课程>-知识体系.md`）。
- `scripts/extract_text.py`：从英文 Word/PPT 抽取全文（`dump` 子命令，按扩展名自动分发）。
- `scripts/reflect_path.py`：路径助手（`content/Raw` → `content/Reflect` 映射，按文件建文件夹；`--mkdir` 首次映射课程时自动创建课程级 `讲解原则.md`）。
- `scripts/locate_knowledge.py`：跨文件定位知识点（返回文件#锚点链接）。
- `scripts/course_summary.py`：枚举课程目录下各课件知识点摘要，提取 `sm-N` 主题供生成课程知识体系。
- `scripts/md_to_docx.py`：把 Markdown 转为高可读性的 `.docx`（可按需手动把讲解/摘要 md 转 Word）。

## 功能

- 英文 Word/PPT 直接总结讲解（`summarize-knowledge`）：不经翻译，直接阅读理解英文源文件，生成中文细粒度讲解 + 粗粒度摘要两份 md，含知识点间联系与锚点链接；讲解面向大一/大二、按难度分级展开，抽象/硬核概念用「直觉→是什么→为什么→怎么用→类比→易错点→前置」分层讲解并增加篇幅、通俗化；每个讲解点附英文原文——已实现。
- 跨文件知识点定位（`locate-knowledge`）：按关键字返回文件#锚点链接——已实现。
- 课程级知识体系（`course-summary`）：汇总各课件摘要，展现跨课件联系并附 Mermaid 图谱——已实现。
- 一键编排（`summary`）：对一份英文文件按「讲解 → 总结」串行执行——已实现。

## 更新记录

- 2026-10-01 — 移除翻译流程，改为直接对英文 PPT/Word 总结讲解：删除 `translate-word`/`translate-ppt`/`translate-pdf` 三个 skill 及其脚本/测试、`scripts/termbase.py`/`symbols.json`/`garbage.json`/`test_termbase.py`、`glossary/`、`tm/`；新增 `scripts/extract_text.py`（抽取英文全文）；`summarize-knowledge` 改为英文输入（不翻译）；`summary` 编排改为「讲解 → 总结」两步；`reflect_path.py` 产物精简为 `全文.txt`/`专有名词.md`/`知识点讲解.md`/`知识点摘要.md`；术语统一改由每文件专有名词对照表承担；清空 `content/Reflect/` 后对 8 份英文 PPT 重新生成。
- 2026-10-01 — 从改进版复用 9.30 讲解逻辑与工作流更新（拆分 SKILL.md、课程级讲解原则机制、讲解规范与专业名词门槛、移除自动生成 Word 版），详见以下各条。
- 2026-10-01 — 移除 `summarize-knowledge` 讲解流程中自动调用 `md_to_docx.py` 生成 Word 版的步骤（讲解只输出两份 md，Word 版不再自动生成；`scripts/md_to_docx.py` 保留、可按需手动使用）。
- 2026-10-01 — 为 `summarize-knowledge` 讲解新增「专业名词门槛」准则：讲解正文避免出现超出读者先修范围的专业名词，仅在（已在本课程出现 / 已被高数与高中及以前知识覆盖 / 必须引入且当场解释）三种情况允许使用。
- 2026-10-01 — 改进 `summarize-knowledge` 讲解规范：明确受众为大一/大二、按难度分级展开、必要时增加篇幅并通俗化（每个讲解点用「直觉/是什么/为什么/怎么用/类比/易错点/前置」行内加粗标签分层，保持 `kp-N` 锚点与英文原文标题不变）。
- 2026-10-01 — AIE1903、AIE2040 课程级讲解原则增加条目：即使课程文件没有给出，讲解定理/算法时应给出相关公式并注明各参数意义。
- 2026-10-01 — 新增课程级讲解原则机制：每门课程映射目录 `content/Reflect/<课程>/` 下可放 `讲解原则.md` 记录课程特定讲解要求（优先级 `CLAUDE.md` > 课程级 > 全局 `知识点讲解原则.md`）；`reflect_path.py --mkdir` 首次映射时自动创建模板，并为 AIE1903/AIE2040/GEC3407 补建。
- 2026-10-01 — 拆分 `summarize-knowledge` 的 `SKILL.md` 为三个文件：`SKILL.md` 仅保留触发/输入/工作流程，另建 `知识点讲解原则.md`（细粒度讲解规则）与 `知识点总结原则.md`（粗粒度摘要规则）；执行时按需查询对应原则文件。
- 2026-09-28 — 全项目审计后修复数据污染与功能 bug（P0+P1）：① `symbols.json` 符号规范化改为**仅对公式段落生效**（两个翻译脚本 `_normalize_part` 加 `_is_formula` 门槛），杜绝误伤代码 `__init__` 与中文「耽误/聂」；② `termbase.py` 新增 `prune-tm` 清理 TM 脏条目（删除 68 条无字母/单字符/自映射/错配键，现有 ~3656 条）；③ 修复 AIE2040 已污染产物「右移—⁻¹0 → 右移—10」；④ 修 `locate_knowledge.py` 锚点跨节错位、`md_to_docx.py` 剥行内反引号 + 表格 + 图片感叹号 + 标题/表头真正加粗与字号、`course_summary.py` 容错（锚点属性/加粗概括/多级标题）+ 空主题告警。新增 `test_locate_knowledge.py`/`test_course_summary.py`/`test_md_to_docx.py`，翻译测试增至 29/29、19/19。
- 2026-09-28 — 对 `content/Raw/AIE1903/` 的两份 PPT 执行 `summary` 全流程（翻译→讲解→总结）：`L1 Input Processing (1)`（436 段，译 296）、`L2-MLP CNN Transformer(1)`（794 段，译 454），均 verify 4/4；每份产出成品 + `全文.txt`/`段落.json`/`对照审校.md`/`专有名词.md`/`知识点讲解.md`（含 Word 版）/`知识点摘要.md`，并生成课程级 `AIE1903-知识体系.md`（含 Mermaid 图谱）。新建 `glossary/AIE1903.md`（46 条术语）。翻译记忆累积至 ~3700 条。另修复符号规范化 `__→−` 规则对 Python 代码 `__init__` 的 6 处误伤。
- 2026-09-26 — 增强 `summarize-knowledge`：每个讲解点标题附该概念的英文原文（`中文名（English term）`）；生成讲解 md 后同步输出高可读性 Word 版。新增 `scripts/md_to_docx.py`（Markdown→docx），并对现有 5 份讲解 md 补英文原文 + 生成 `.docx`。
- 2026-09-26 — 对 AIE2040 课件 `probability-statistics-ai-lecture [Repaired].pptx` 执行 `summery` 全流程：翻译 898 段（概率与统计，verify 4/4）、生成知识讲解+摘要两份 md、生成课程级 `AIE2040-知识体系.md`；新建 `glossary/AIE2040.md`（48 条术语）。翻译记忆累积至 ~3000 条。
- 2026-09-26 — 对 4 份 quiz 版 PPT 执行 `summery` 全流程（翻译→讲解→总结）：Ch_1quiz（105 段）、Ch_2 QUIZ（142 段）、L4 QUIZ（124 段）、TOPIC 3 quiz（171 段），均 verify 4/4，并生成课程级 `GEC3407-知识体系.md`（含 Mermaid 图谱）。翻译记忆累积至 ~2300 条。
- 2026-09-26 — 新增编排 skill `summery`：对一份文件自动判断类型，严格按「翻译 → 讲解 → 总结」串行执行 translate / summarize-knowledge / course-summary，前一步完成并校验通过后才执行下一步。
- 2026-09-26 — 新增 `course-summary` skill（课程级知识体系总结，汇总各课件 `知识点摘要.md`，展现跨课件联系并附 Mermaid 图谱）+ `scripts/course_summary.py`；`summarize-knowledge` 工作流末尾补「更新课程知识体系」一步。
- 2026-09-26 — 对 `content/Raw/GEC3407/` 的 4 份 PPT 执行「翻译 + 知识总结」：Chapter 3（214 段）、TOPIC 2（250 段）、TOPIC1（912 段）、TOPIC4（349 段），每份产出成品 + `全文.txt`/`段落.json`/`对照审校.md`/`专有名词.md`/`知识点讲解.md`/`知识点摘要.md`，`verify` 均 4/4。翻译记忆累积至 ~1900 条。
- 2026-09-26 — 新增 `summarize-knowledge`（知识点总结与讲解，一次生成细粒度讲解 + 粗粒度摘要两份 md，摘要内嵌锚点链接）与 `locate-knowledge`（跨文件定位知识点）+ `scripts/locate_knowledge.py`；`reflect_path.py` 新增 `knowledge_detail`/`knowledge_summary`。
- 2026-09-26 — 新增过程产物「专有名词对照表」：翻译前完整浏览文件并汇总专有名词（英文→中文）到 `文件名-专有名词.md`，作为该文件翻译与后续讲解的统一标准；`reflect_path.py` 新增 `proper_nouns` 路径。
- 2026-09-26 — 明确项目目标：不仅翻译课件，还要对所有知识进行归纳整理与讲解，迅速串联知识、建立知识体系（已同步到 `CLAUDE.md` 与项目简介）。
- 2026-09-26 — 修复垃圾清理误伤：`兰` 标记会误清空含「法兰克福/波兰」等词的段落（GEC3407 的「法兰克福学派」曾被清空），改为仅对公式段落生效；重跑已恢复，测试增至 27/27。
- 2026-09-26 — 更新导出方式：源文件存 `content/Raw/<子目录>/`，译文映射到 `content/Reflect/<子目录>/<文件名>/`（按文件建文件夹，含成品 + `全文.txt`/`段落.json`/`对照审校.md`/`新增术语.json`），新增 `scripts/reflect_path.py` 路径助手；两个 skill 的 SKILL.md 已同步。
- 2026-09-26 — 三项改进：① `normalize` 集成进 `apply`（翻译写回时自动规范化+清理）；② `_hint` 增加 `mixed`（中英混排段落翻译英文、保留中文）；③ 新增 `scripts/garbage.json` 垃圾清理（Slide20 的 25 处乱码页脚 `b = 9 兰` 已清空）。测试 ppt 26/26、word 17/17。
- 2026-09-26 — 明确「非文本内容不译」规则：两个 skill 硬性约束新增第 6 条（公式/符号/数字/单位/代码等一律原样保留），`extract` 输出增加 `formula` 启发式标记。
- 2026-09-26 — 实现符号规范化（持久化、可扩展）：新建 `scripts/symbols.json`，`termbase.py` 增加 `symbols-list/add/detect`，两个 skill 增加 `normalize` 子命令。对 `Slide20-中文.pptx` 套用后修复 98 处乱码符号（耽→ℝ、丄→⊥、聂→‖、__→−、—1→⁻¹），`verify` 4/4 通过。
- 2026-09-26 — 首次真实翻译 PPT：`Slide20.pptx`（MAT2040 线性代数·正交性 II）→ `Chinese/Slide20-中文.pptx`（221 段中译 127、保留 94 段公式/符号/页脚等），`verify` 4/4 通过。新建 `glossary/MAT2040.md`（37 条术语）。源 PPT 含 PDF 转换产生的符号错乱（耽=ℝ、丄=⊥、聂=‖·‖ 等），按 C7 规则原样保留未改写。
- 2026-09-26 — 实现 `translate-ppt`：迁移 `translate-word` 的算法（w:t→a:t、w:rPr→a:rPr、字号改 `a:rPr@sz`），支持多部件（幻灯片+备注）遍历，复用术语表/翻译记忆/校验/审校；端到端测试 18/18 通过。
- 2026-09-26 — 首次真实翻译完成：`GEC3407 COURSE OUTLINE.docx` → `Chinese/GEC3407 COURSE OUTLINE-中文.docx`（363 段中译 309、保留 54 段编号/日期/等级/引文），`verify` 4/4 通过。修复 `<w:t/>` 自闭合标签的正则误吞 bug（校验曾误报结构不一致），测试补强同格式双 run 用例。
- 2026-09-26 — 更新 `translate-word` 输出约定：译文以 `原名-中文.docx` 存 `Chinese/`，不覆盖原文档；`apply` 增加「同路径拒绝覆盖」与「自动创建输出目录」兜底；测试增至 17/17 通过。
- 2026-09-26 — 完成 C/D/E 安全项：`translate-word` 新增 `verify`（只读校验：图片/结构/字号）与 `review`（原文/译文对照审校），并明确公式/数字/单位不译规则；测试增至 15/15 通过。
- 2026-09-26 — 完成 B 项：建立项目级术语表（`glossary/`，按课程）与翻译记忆（`tm/`），新增共享工具 `scripts/termbase.py`（init/merge-glossary、fill/save-tm），供三个 skill 复用，保证术语与译文跨文件、跨课程一致。
- 2026-09-26 — `translate-word` 完成 A 项加固：`apply` 改为定点替换（其余字节不变）、保留行内格式（同格式合并 / 异格式按比例分配）、新增端到端测试（13/13 通过）。
- 2026-09-26 — 完善 `translate-word`：翻译前须完整浏览全文、提炼领域与要点，并建立术语对照表，保证专有名词准确且前后一致。
- 2026-09-26 — 编写 `translate-word` skill：抽取段落→翻译英文段落→写回，纯标准库脚本，保留图片/字号/文本框位置。
- 2026-09-26 — 记录项目目的与工作方式：整理各科学习资料、串联知识点；输入为英文 PPT/Word/PDF，当前阶段为完整翻译。
- 2026-09-26 — 初始化：建立 `CLAUDE.md` 与 `Readme.md`，确立「项目操作须同步 Readme.md」原则。
