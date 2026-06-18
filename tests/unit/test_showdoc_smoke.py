from pathlib import Path
import subprocess
import sys

import pytest
import yaml

from utils.showdoc_smoke import (
    build_smoke_cases,
    classify_case_risk,
    normalize_placeholder_values,
    parse_showdoc_markdown,
    write_smoke_cases_yaml,
)

pytestmark = pytest.mark.unit

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_parse_showdoc_markdown_extracts_core_request_contract(tmp_path: Path):
    doc = tmp_path / "10950_域名切换查询接口.md"
    doc.write_text(
        """---
page_id: "10950"
page_title: "域名切换查询接口"
catalog_path:
  - "基础功能支持"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=10950"
---
# 域名切换查询接口

**请求URL：**
- `/public/domain-switch`

**请求方式：**
- `POST`
- `RequestBody`

### 请求参数Json格式

```json
{
 "groupCode":"String",
 "currentBaseUrl":"String",
 "clientVersion":"String"
}
```

### 响应参数

|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|Object||
|msg|否|String||
|code|否|String||
|traceId|否|String||
""",
        encoding="utf-8",
    )

    endpoint = parse_showdoc_markdown(doc)

    assert endpoint.page_id == "10950"
    assert endpoint.title == "域名切换查询接口"
    assert endpoint.catalog_path == ["基础功能支持"]
    assert endpoint.method == "POST"
    assert endpoint.raw_method == "POST"
    assert endpoint.url == "/public/domain-switch"
    assert endpoint.request_body == {
        "groupCode": "String",
        "currentBaseUrl": "String",
        "clientVersion": "String",
    }
    assert endpoint.response_fields == ["data", "msg", "code", "traceId"]


def test_parse_showdoc_markdown_treats_all_method_as_post(tmp_path: Path):
    doc = tmp_path / "all_method.md"
    doc.write_text(
        """# 通用接口

**请求URL：**
- `/app/example`

**请求方式：**
- ALL

### 请求参数Json格式

```
{}
```
""",
        encoding="utf-8",
    )

    endpoint = parse_showdoc_markdown(doc)

    assert endpoint.raw_method == "ALL"
    assert endpoint.method == "POST"


def test_parse_showdoc_markdown_normalizes_url_without_leading_slash(tmp_path: Path):
    doc = tmp_path / "05585_自定义添加会员服务.md"
    doc.write_text(
        """# 自定义添加会员服务

**请求URL：**
- `core/app/Business/member/addMemberService `

**请求方式：**
- POST
""",
        encoding="utf-8",
    )

    endpoint = parse_showdoc_markdown(doc)

    assert endpoint.url == "/core/app/Business/member/addMemberService"


def test_build_smoke_cases_skips_docs_without_url(tmp_path: Path):
    valid_doc = tmp_path / "valid.md"
    valid_doc.write_text(
        """---
page_id: "1"
page_title: "有效接口"
---
# 有效接口

**请求URL：**
- `/valid/url`

**请求方式：**
- POST
""",
        encoding="utf-8",
    )
    invalid_doc = tmp_path / "invalid.md"
    invalid_doc.write_text("# 不是接口文档\n", encoding="utf-8")

    cases = build_smoke_cases(tmp_path)

    assert len(cases) == 1
    assert cases[0]["page_id"] == "1"
    assert cases[0]["url"] == "/valid/url"
    assert cases[0]["method"] == "POST"
    assert cases[0]["risk_level"] == "read"


def test_build_smoke_cases_marks_mutation_endpoints(tmp_path: Path):
    doc = tmp_path / "delete.md"
    doc.write_text(
        """---
page_id: "2"
page_title: "会员商城删除会员笔记或评论"
---
# 会员商城删除会员笔记或评论

**请求URL：**
- `/community/member/note/delete`

**请求方式：**
- POST
""",
        encoding="utf-8",
    )

    cases = build_smoke_cases(tmp_path)

    assert cases[0]["risk_level"] == "mutation"


@pytest.mark.parametrize(
    ("title", "url", "expected"),
    [
        ("优惠券列表", "/app/Business/member/coupon/list", "read"),
        ("获取话题分类", "/community/topic/category/list", "read"),
        ("会员商城删除会员笔记或评论", "/community/member/note/delete", "mutation"),
        ("保存门店实体卡价格清单设置", "/mem/entityCardPrice/save", "mutation"),
    ],
)
def test_classify_case_risk(title: str, url: str, expected: str):
    assert classify_case_risk(title, url) == expected


def test_normalize_placeholder_values_uses_project_payload_defaults():
    payload = {
        "tokenId": "String",
        "memberId": "String",
        "pageIndex": 0,
        "enabled": True,
        "items": [{"name": "String"}],
    }

    assert normalize_placeholder_values(payload) == {
        "tokenId": "",
        "memberId": "",
        "pageIndex": 0,
        "enabled": True,
        "items": [{"name": ""}],
    }


def test_write_smoke_cases_yaml_writes_project_style_sections(tmp_path: Path):
    output = tmp_path / "cases.yaml"
    cases = [
        {
            "page_id": "1",
            "title": "有效接口",
            "catalog_path": [],
            "method": "POST",
            "raw_method": "POST",
            "url": "/valid/url",
            "request_body": {},
            "response_fields": ["data", "msg"],
            "risk_level": "read",
            "source_file": "valid.md",
            "source_url": "",
        }
    ]

    write_smoke_cases_yaml(cases, output)

    loaded = yaml.safe_load(output.read_text(encoding="utf-8"))
    assert loaded == {
        "showdoc_1": {
            "_meta": {
                "page_id": "1",
                "title": "有效接口",
                "catalog_path": [],
                "method": "POST",
                "raw_method": "POST",
                "url": "/valid/url",
                "response_fields": ["data", "msg"],
                "risk_level": "read",
                "source_file": "valid.md",
                "source_url": "",
            }
        }
    }


def test_generate_showdoc_smoke_cases_script_runs_from_project_root(tmp_path: Path):
    source = tmp_path / "docs"
    source.mkdir()
    (source / "valid.md").write_text(
        """---
page_id: "1"
page_title: "有效接口"
---
# 有效接口

**请求URL：**
- `/valid/url`

**请求方式：**
- POST
""",
        encoding="utf-8",
    )
    output = tmp_path / "cases.yaml"

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "generate_showdoc_smoke_cases.py"),
            "--source",
            str(source),
            "--output",
            str(output),
        ],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "已生成 1 条冒烟用例" in result.stdout
    loaded = yaml.safe_load(output.read_text(encoding="utf-8"))
    assert loaded["showdoc_1"]["_meta"]["url"] == "/valid/url"
