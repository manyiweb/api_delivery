"""从 ShowDoc Markdown 目录生成冒烟测试 YAML 数据。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.showdoc_smoke import build_smoke_cases, write_smoke_cases_yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 ShowDoc 冒烟测试 YAML 数据")
    parser.add_argument("--source", required=True, help="ShowDoc Markdown 目录")
    parser.add_argument("--output", required=True, help="输出 YAML 文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases = build_smoke_cases(Path(args.source))
    write_smoke_cases_yaml(cases, Path(args.output))
    print(f"已生成 {len(cases)} 条冒烟用例: {args.output}")


if __name__ == "__main__":
    main()
