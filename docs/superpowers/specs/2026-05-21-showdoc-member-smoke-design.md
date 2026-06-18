# 店务助手会员接口冒烟用例转换设计

## 目标

将 `docs/showdoc/店务助手_智慧收银台/会员` 下的 ShowDoc 接口文档转换为可执行的冒烟测试用例，先完成一个小范围试点，验证后续扩展到更多目录的可行性。

## 范围

- 输入范围：`docs/showdoc/店务助手_智慧收银台/会员` 下的 57 个 Markdown 接口文档。
- 输出数据：`data/showdoc_member_smoke_cases.yaml`。
- 输出用例：`case/test_showdoc_member_smoke.py`。
- 不修改 ShowDoc 导出文档本身。
- 不处理跨接口业务链路依赖，只做单接口探活冒烟。

## 方案

新增一个轻量解析模块，负责从 Markdown 中提取接口标题、page_id、目录路径、请求 URL、请求方法、请求体示例和响应字段。生成器将解析结果写入 YAML，pytest 用例从 YAML 读取并参数化执行。

请求体优先使用文档中的“请求参数Json格式”。若示例是合法 JSON，则按原结构保留；常见占位值暂不做复杂替换，只在运行时补充 `tokenId` 字段为当前 `access_token`，降低对业务数据的侵入。方法为 `ALL` 的接口先按 `POST` 执行，并在 YAML 中保留原始方法，便于后续调整。

## 断言

冒烟断言保持低风险：

- HTTP 状态码小于 500。
- 响应内容必须是 JSON。
- 响应 JSON 至少包含文档声明响应字段中的一个，或包含常见业务字段 `code`、`msg`、`data`、`success` 中的一个。

该策略的目标是尽早发现接口不可达、网关异常、非 JSON 响应和明显契约漂移，不强行断言业务成功，避免因缺少真实业务数据导致试点大量误报。

## 测试

- 为 Markdown 解析和 YAML 生成添加本地单元测试，不访问外部接口。
- 运行 `pytest tests/unit -q` 验证解析逻辑和现有护栏。
- 可按需运行 `pytest case/test_showdoc_member_smoke.py -m smoke` 执行真实接口冒烟。
