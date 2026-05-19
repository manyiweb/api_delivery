from pathlib import Path
from types import SimpleNamespace

import pytest

import conftest

pytestmark = pytest.mark.unit


def _request_with_paths(*paths):
    items = [SimpleNamespace(path=Path(path)) for path in paths]
    return SimpleNamespace(session=SimpleNamespace(items=items))


def test_unit_only_session_is_detected_from_collected_paths():
    request = _request_with_paths(
        "tests/unit/test_allure_helper.py",
        "tests/unit/test_conftest.py",
    )

    assert conftest._is_unit_only_session(request) is True


def test_mixed_or_case_session_is_not_unit_only():
    request = _request_with_paths(
        "tests/unit/test_allure_helper.py",
        "case/test_mt_order.py",
    )

    assert conftest._is_unit_only_session(request) is False
