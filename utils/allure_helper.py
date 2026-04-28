"""Allure report helpers used by tests and API wrappers."""
import json
from typing import Any

import allure


def step(title: str):
    """Return an Allure step context manager."""
    return allure.step(title)


def attach_text(name: str, value: Any) -> None:
    """Attach a value to Allure as plain text."""
    allure.attach(
        "" if value is None else str(value),
        name=name,
        attachment_type=allure.attachment_type.TEXT,
    )


def attach_json(name: str, data: Any) -> None:
    """Attach JSON-like data to Allure with readable formatting."""
    allure.attach(
        json.dumps(data, ensure_ascii=False, indent=2, default=str),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )
