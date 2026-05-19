from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_jenkins_does_not_mask_pytest_failures():
    jenkinsfile = (PROJECT_ROOT / "Jenkinsfile").read_text(encoding="utf-8")

    assert "|| exit 0" not in jenkinsfile
    assert "currentBuild.result = 'SUCCESS'" not in jenkinsfile
    assert "-m smoke" in jenkinsfile


def test_core_business_cases_are_marked_for_smoke_gate():
    mt_order = (PROJECT_ROOT / "case" / "test_mt_order.py").read_text(encoding="utf-8")
    invoice = (PROJECT_ROOT / "case" / "test_saas_Invoice.py").read_text(encoding="utf-8")
    pay = (PROJECT_ROOT / "case" / "test_saas_pay.py").read_text(encoding="utf-8")

    assert "@pytest.mark.smoke" in mt_order
    assert "@pytest.mark.smoke" in invoice
    assert "@pytest.mark.smoke" in pay
