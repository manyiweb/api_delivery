import pytest

from utils.auth import normalize_login_word

pytestmark = pytest.mark.unit


def test_normalize_login_word_hashes_plain_password():
    assert normalize_login_word("123456") == "e10adc3949ba59abbe56e057f20f883e"


def test_normalize_login_word_keeps_existing_md5_lowercase():
    assert normalize_login_word("E10ADC3949BA59ABBE56E057F20F883E") == "e10adc3949ba59abbe56e057f20f883e"


def test_normalize_login_word_strips_whitespace_before_hashing():
    assert normalize_login_word(" 123456 \n") == "e10adc3949ba59abbe56e057f20f883e"
