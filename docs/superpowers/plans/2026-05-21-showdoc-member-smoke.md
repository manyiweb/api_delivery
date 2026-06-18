# ShowDoc Member Smoke Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `docs/showdoc/店务助手_智慧收银台/会员` 接口文档转换成数据驱动冒烟测试。

**Architecture:** 新增一个独立的 ShowDoc 解析与 YAML 生成模块，pytest 用例只负责读取 YAML、发送请求和做低风险冒烟断言。生成脚本可重复执行，后续扩目录时只替换输入目录和输出文件。

**Tech Stack:** Python 3、pytest、httpx、PyYAML、allure-pytest。

---

### Task 1: 解析 ShowDoc Markdown

**Files:**
- Create: `utils/showdoc_smoke.py`
- Test: `tests/unit/test_showdoc_smoke.py`

- [ ] **Step 1: Write failing parser tests**

编写单元测试，覆盖提取 `page_id`、标题、URL、方法、请求 JSON 和响应字段。

- [ ] **Step 2: Run parser tests and confirm failure**

运行：`pytest tests/unit/test_showdoc_smoke.py -q`

预期：因 `utils.showdoc_smoke` 不存在而失败。

- [ ] **Step 3: Implement parser**

实现 `parse_showdoc_markdown(path)` 和相关数据结构，保持解析逻辑聚焦。

- [ ] **Step 4: Run parser tests**

运行：`pytest tests/unit/test_showdoc_smoke.py -q`

预期：解析相关测试通过。

### Task 2: 生成会员冒烟 YAML

**Files:**
- Modify: `utils/showdoc_smoke.py`
- Create: `scripts/generate_showdoc_smoke_cases.py`
- Create: `data/showdoc_member_smoke_cases.yaml`
- Test: `tests/unit/test_showdoc_smoke.py`

- [ ] **Step 1: Write failing generator tests**

覆盖目录生成、跳过无 URL 文档、写出 YAML 的字段结构。

- [ ] **Step 2: Run generator tests and confirm failure**

运行：`pytest tests/unit/test_showdoc_smoke.py -q`

预期：生成函数不存在或行为未实现而失败。

- [ ] **Step 3: Implement generator and CLI script**

实现 `build_smoke_cases(source_dir)` 与脚本入口。

- [ ] **Step 4: Generate YAML**

运行：`python3 scripts/generate_showdoc_smoke_cases.py --source "docs/showdoc/店务助手_智慧收银台/会员" --output data/showdoc_member_smoke_cases.yaml`

预期：生成 57 条冒烟用例数据。

### Task 3: 新增 pytest 冒烟用例

**Files:**
- Create: `case/test_showdoc_member_smoke.py`
- Modify: `tests/unit/test_core_guardrails.py`

- [ ] **Step 1: Write guardrail test**

补充单元测试，确认会员 ShowDoc 冒烟用例存在并带有 `@pytest.mark.smoke`。

- [ ] **Step 2: Run guardrail test and confirm failure**

运行：`pytest tests/unit/test_core_guardrails.py -q`

预期：因冒烟用例文件不存在而失败。

- [ ] **Step 3: Implement pytest case**

读取 `data/showdoc_member_smoke_cases.yaml`，参数化调用接口，补充 `tokenId`，并执行低风险断言。

- [ ] **Step 4: Run unit tests**

运行：`pytest tests/unit -q`

预期：本地单元测试全部通过。

### Task 4: 验证真实冒烟试点

**Files:**
- No code changes expected.

- [ ] **Step 1: Run smoke trial**

运行：`pytest case/test_showdoc_member_smoke.py -m smoke -q`

预期：如果当前环境和测试数据允许，接口冒烟执行完成；若存在业务数据或环境失败，记录失败原因。
