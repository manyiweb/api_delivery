"""ShowDoc 接口文档转冒烟用例的工具函数。"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml

MUTATION_KEYWORDS = (
    "add",
    "audit",
    "cancel",
    "delete",
    "edit",
    "give",
    "publish",
    "reorder",
    "review",
    "save",
    "update",
    "useCancel",
    "作废",
    "保存",
    "发布",
    "回复",
    "审批",
    "撤销",
    "新增",
    "核销",
    "派发",
    "点赞",
    "收藏",
    "记录是否勾选",
    "转增",
    "删除",
)


@dataclass(frozen=True)
class ShowDocEndpoint:
    """单个 ShowDoc 接口文档解析结果。"""

    page_id: str
    title: str
    catalog_path: list[str]
    method: str
    raw_method: str
    url: str
    request_body: Any
    response_fields: list[str]
    source_file: str
    source_url: str

    def to_case(self) -> dict[str, Any]:
        """转换为 YAML 冒烟用例结构。"""
        data = asdict(self)
        data["risk_level"] = classify_case_risk(self.title, self.url)
        return data


def classify_case_risk(title: str, url: str) -> str:
    """按标题和路径粗略判断冒烟接口是否可能产生写操作。"""
    text = f"{title} {url}"
    lower_text = text.lower()
    for keyword in MUTATION_KEYWORDS:
        if keyword.lower() in lower_text:
            return "mutation"
    return "read"


def normalize_placeholder_values(value: Any) -> Any:
    """将 ShowDoc 占位值转换成项目 YAML 常用默认值。"""
    if isinstance(value, dict):
        return {key: normalize_placeholder_values(item) for key, item in value.items()}

    if isinstance(value, list):
        return [normalize_placeholder_values(item) for item in value]

    if value == "String":
        return ""

    return value


def _case_key(case: dict[str, Any]) -> str:
    page_id = str(case.get("page_id") or "").strip()
    if page_id:
        return f"showdoc_{page_id}"

    url = str(case.get("url") or "unknown").strip("/")
    normalized = re.sub(r"[^0-9A-Za-z]+", "_", url).strip("_").lower()
    return f"showdoc_{normalized or 'unknown'}"


def to_project_style_cases(cases: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """转换为项目现有 YAML 风格：顶层配置段内直接放请求参数。"""
    result: dict[str, dict[str, Any]] = {}

    for case in cases:
        payload = normalize_placeholder_values(case.get("request_body", {}))
        if not isinstance(payload, dict):
            payload = {"body": payload}

        section = dict(payload)
        section["_meta"] = {
            "page_id": case.get("page_id", ""),
            "title": case.get("title", ""),
            "catalog_path": case.get("catalog_path", []),
            "method": case.get("method", "POST"),
            "raw_method": case.get("raw_method", "POST"),
            "url": case.get("url", ""),
            "response_fields": case.get("response_fields", []),
            "risk_level": case.get("risk_level", "read"),
            "source_file": case.get("source_file", ""),
            "source_url": case.get("source_url", ""),
        }
        result[_case_key(case)] = section

    return result


def _extract_front_matter(text: str) -> dict[str, Any]:
    match = re.match(r"^---\n(?P<body>[\s\S]*?)\n---", text)
    if not match:
        return {}

    result: dict[str, Any] = {}
    lines = match.group("body").splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        key_value = re.match(r"^(?P<key>[A-Za-z_][\w-]*):\s*(?P<value>.*)$", line)
        if not key_value:
            index += 1
            continue

        key = key_value.group("key")
        value = key_value.group("value").strip()
        if value:
            result[key] = value.strip('"')
            index += 1
            continue

        values: list[str] = []
        index += 1
        while index < len(lines):
            item = re.match(r'^\s*-\s*"?(?P<value>.*?)"?\s*$', lines[index])
            if not item:
                break
            values.append(item.group("value"))
            index += 1
        result[key] = values

    return result


def _extract_title(text: str, front_matter: dict[str, Any], fallback: str) -> str:
    if front_matter.get("page_title"):
        return str(front_matter["page_title"]).strip()

    match = re.search(r"^#\s+(?P<title>.+?)\s*$", text, re.MULTILINE)
    if match:
        return match.group("title").strip()

    return fallback


def _extract_url(text: str) -> str:
    url_block = re.search(r"\*\*请求URL：\*\*([\s\S]*?)(?:\n\s*\n|\*\*请求方式：\*\*)", text)
    search_area = url_block.group(1) if url_block else text
    match = re.search(r"-\s*`?(?P<url>[^`\n\r]+)`?", search_area)
    if not match:
        return ""
    url = match.group("url").strip()
    if not url:
        return ""
    return url if url.startswith("/") else f"/{url}"


def _extract_method(text: str) -> tuple[str, str]:
    method_block = re.search(r"\*\*请求方式：\*\*([\s\S]*?)(?:\n\s*\n|###)", text)
    if not method_block:
        return "POST", "POST"

    match = re.search(r"-\s*`?(?P<method>[A-Z]+)`?", method_block.group(1))
    raw_method = match.group("method") if match else "POST"
    method = "POST" if raw_method == "ALL" else raw_method
    return method, raw_method


def _extract_json_after_heading(text: str, heading_pattern: str) -> Any:
    heading = re.search(heading_pattern, text)
    if not heading:
        return {}

    code_block = re.search(r"```(?:json)?\s*(?P<json>[\s\S]*?)```", text[heading.end() :], re.IGNORECASE)
    if not code_block:
        return {}

    raw_json = code_block.group("json").strip()
    if not raw_json:
        return {}

    normalized = raw_json.replace(": boolean", ": false")
    try:
        return json.loads(normalized)
    except json.JSONDecodeError:
        return {}


def _extract_response_fields(text: str) -> list[str]:
    response_heading = re.search(r"###\s*(?:返回参数|响应参数)", text)
    if not response_heading:
        return []

    tail = text[response_heading.end() :]
    next_heading = re.search(r"\n###\s+", tail)
    table_area = tail[: next_heading.start()] if next_heading else tail
    fields: list[str] = []

    for line in table_area.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or cells[0] in {"参数名", ":----", ""}:
            continue
        field = cells[0].lstrip("-").strip()
        if field and field not in fields:
            fields.append(field)

    return fields


def parse_showdoc_markdown(path: Path | str) -> ShowDocEndpoint:
    """解析单个 ShowDoc Markdown 接口文档。"""
    doc_path = Path(path)
    text = doc_path.read_text(encoding="utf-8-sig")
    front_matter = _extract_front_matter(text)
    method, raw_method = _extract_method(text)

    return ShowDocEndpoint(
        page_id=str(front_matter.get("page_id", "")),
        title=_extract_title(text, front_matter, doc_path.stem),
        catalog_path=list(front_matter.get("catalog_path", [])),
        method=method,
        raw_method=raw_method,
        url=_extract_url(text),
        request_body=_extract_json_after_heading(text, r"###\s*请求参数Json格式"),
        response_fields=_extract_response_fields(text),
        source_file=str(doc_path),
        source_url=str(front_matter.get("source_url", "")),
    )


def iter_markdown_files(source_dir: Path | str) -> Iterable[Path]:
    """按文件名稳定遍历 Markdown 接口文档。"""
    return sorted(Path(source_dir).rglob("*.md"))


def build_smoke_cases(source_dir: Path | str) -> list[dict[str, Any]]:
    """从目录构建可执行的冒烟用例数据。"""
    cases: list[dict[str, Any]] = []
    for markdown_file in iter_markdown_files(source_dir):
        endpoint = parse_showdoc_markdown(markdown_file)
        if not endpoint.url:
            continue
        cases.append(endpoint.to_case())
    return cases


def write_smoke_cases_yaml(cases: list[dict[str, Any]], output_path: Path | str) -> None:
    """将冒烟用例数据写入 YAML 文件。"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(to_project_style_cases(cases), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
