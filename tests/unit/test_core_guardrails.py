from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.unit

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_ci_does_not_mask_pytest_failures():
    gitlab_ci = (PROJECT_ROOT / ".gitlab-ci.yml").read_text(encoding="utf-8")

    assert "|| exit 0" not in gitlab_ci
    assert "|| true" not in gitlab_ci
    assert "-m smoke" in gitlab_ci
    # smoke/critical 是门禁，不能设置 allow_failure: true
    assert "allow_failure: true" not in gitlab_ci


def test_ci_allows_agent_triggered_api_tests_to_be_non_blocking():
    gitlab_ci = (PROJECT_ROOT / ".gitlab-ci.yml").read_text(encoding="utf-8")

    assert "API_TEST_NON_BLOCKING" in gitlab_ci
    assert "CI_PIPELINE_SOURCE" in gitlab_ci
    assert "[ \"$CI_PIPELINE_SOURCE\" = \"trigger\" ]" in gitlab_ci
    assert "[ -n \"$UPSTREAM_PROJECT\" ]" in gitlab_ci
    assert "[ -n \"$TRIGGER_SOURCE_PROJECT\" ]" in gitlab_ci


def test_real_api_regression_does_not_run_on_api_project_push():
    gitlab_ci = yaml.safe_load((PROJECT_ROOT / ".gitlab-ci.yml").read_text(encoding="utf-8"))

    for job_name in ("smoke", "critical", "allure_report", "pages", "notify"):
        only_refs = gitlab_ci[job_name]["only"]
        assert "triggers" in only_refs
        assert "schedules" in only_refs
        assert "master" not in only_refs
        assert "branches" not in only_refs


def test_wechat_notify_runs_for_every_pipeline_result():
    gitlab_ci = yaml.safe_load((PROJECT_ROOT / ".gitlab-ci.yml").read_text(encoding="utf-8"))

    assert gitlab_ci["notify"]["when"] == "always"


def test_allure_report_flattens_nested_result_artifacts_before_generating():
    gitlab_ci = (PROJECT_ROOT / ".gitlab-ci.yml").read_text(encoding="utf-8")

    assert 'ALLURE_MERGED_RESULTS_DIR: "reports/allure-merged-results"' in gitlab_ci
    assert 'rm -rf "$ALLURE_MERGED_RESULTS_DIR"' in gitlab_ci
    assert 'find "$ALLURE_RESULTS_DIR" -mindepth 2 -type f -exec cp {} "$ALLURE_MERGED_RESULTS_DIR"/ \\;' in gitlab_ci
    assert 'allure generate "$ALLURE_MERGED_RESULTS_DIR" -o "$ALLURE_REPORT_DIR" --clean' in gitlab_ci


def test_legacy_jenkinsfile_removed():
    """迁移到 GitLab CI 后，不应再保留含明文凭证的 Jenkinsfile。"""
    assert not (PROJECT_ROOT / "Jenkinsfile").exists()


def test_core_business_cases_are_marked_for_smoke_gate():
    mt_order = (PROJECT_ROOT / "case" / "test_mt_order.py").read_text(encoding="utf-8")
    invoice = (PROJECT_ROOT / "case" / "test_saas_Invoice.py").read_text(encoding="utf-8")
    pay = (PROJECT_ROOT / "case" / "test_saas_pay.py").read_text(encoding="utf-8")

    assert "@pytest.mark.smoke" in mt_order
    assert "@pytest.mark.smoke" in invoice
    assert "@pytest.mark.smoke" in pay


def test_showdoc_member_smoke_case_is_marked_for_smoke_gate():
    showdoc_member = (PROJECT_ROOT / "case" / "test_showdoc_member_smoke.py").read_text(
        encoding="utf-8"
    )

    assert "@pytest.mark.smoke" in showdoc_member
    assert "showdoc_member_smoke_cases.yaml" in showdoc_member
