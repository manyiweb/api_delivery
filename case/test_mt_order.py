"""Meituan order callback tests.
Covers push, cancel, refund, and idempotency scenarios.
"""
import os

import allure
import pytest

from api.order_callback import (
    mt_cancel_order_callback,
    mt_full_refund_callback,
    mt_push_order_callback,
)
from assertions.order_db_assert import assert_order_count, assert_order_created
from utils.logger import logger


@allure.epic("Meituan API")
@allure.feature("Order callbacks")
class TestMtPushOrder:
    """Order callback scenarios."""

    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.story("Push order")
    @allure.title("Push order callback should create order in DB")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_push_order(self, client, db_conn, cleanup_order):
        """Push order should return OK and create DB record."""
        with allure.step("Send push order callback"):
            logger.info("Start push order")
            result, order_id = mt_push_order_callback(client)
            logger.info(f"Push order result: {result}, order_id: {order_id}")

        with allure.step("Validate push response"):
            allure.attach(
                str(result),
                name="push order response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert result == "OK", f"Push order failed: {result}"
            logger.info("Push order response validated")

        if os.getenv("ENV") == "fat":
            with allure.step("Validate order created in DB"):
                assert_order_created(db_conn, str(order_id), timeout=10)
                cleanup_order.append(str(order_id))
                logger.info(f"Order created in DB: {order_id}")

    @pytest.mark.skip
    @pytest.mark.critical
    @allure.story("Cancel order")
    @allure.title("Cancel callback should update order status")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_cancel_order(self, client, db_conn, cleanup_order):
        """Cancel order should return OK after a successful push."""
        with allure.step("Create order to cancel"):
            logger.info("Create order for cancel test")
            result, order_id = mt_push_order_callback(client)
            logger.info(f"Push order result: {result}, order_id: {order_id}")
            assert result == "OK", "Push order failed; cancel test aborted"

        with allure.step("Wait for order persistence"):
            assert_order_created(db_conn, str(order_id), timeout=10)

        with allure.step("Send cancel callback"):
            logger.info("Start cancel order")
            result = mt_cancel_order_callback(client, order_id)

        with allure.step("Validate cancel response"):
            allure.attach(
                str(result),
                name="cancel order response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert result == "OK", f"Cancel order failed: {result}"
            cleanup_order.append(str(order_id))
            logger.info("Cancel order succeeded")

    @pytest.mark.skip
    @pytest.mark.critical
    @allure.story("Full refund")
    @allure.title("Full refund callback should succeed")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_mt_full_refund(self, client, db_conn, cleanup_order):
        """Full refund should return OK after a successful push."""
        with allure.step("Create order for refund"):
            logger.info("Create order for refund test")
            result, order_id = mt_push_order_callback(client)
            assert result == "OK", "Push order failed; refund test aborted"

        with allure.step("Wait for order persistence"):
            assert_order_created(db_conn, str(order_id), timeout=10)

        with allure.step("Send full refund callback"):
            logger.info("Start full refund")
            result = mt_full_refund_callback(client, order_id)

        with allure.step("Validate full refund response"):
            allure.attach(
                str(result),
                name="full refund response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert result == "OK", f"Full refund failed: {result}"
            cleanup_order.append(str(order_id))
            logger.info("Full refund succeeded")

    @pytest.mark.skip
    @pytest.mark.normal
    @allure.story("Idempotency")
    @allure.title("Duplicate push should be idempotent")
    @allure.severity(allure.severity_level.NORMAL)
    def test_mt_repeat_push_order(self, client, db_conn, cleanup_order):
        """Second push with same order ID should not create duplicates."""
        with allure.step("First push"):
            logger.info("First push order")
            result1, order_id = mt_push_order_callback(client)
            logger.info(f"First push result: {result1}, order_id: {order_id}")

        with allure.step("Validate first push"):
            assert result1 == "OK", f"First push failed: {result1}"
            assert_order_created(db_conn, str(order_id), timeout=10)

        with allure.step("Second push with same order ID"):
            result2, duplicate_order_id = mt_push_order_callback(client, order_id)
            logger.info(
                f"Second push result: {result2}, order_id: {duplicate_order_id}"
            )
            assert duplicate_order_id == order_id, (
                f"Order ID mismatch: {duplicate_order_id} vs {order_id}"
            )

        with allure.step("Validate second push and DB count"):
            assert result2 == "OK", f"Second push failed: {result2}"
            assert_order_count(db_conn, str(order_id), expected_count=1)
            cleanup_order.append(str(order_id))
            logger.info("Idempotency validated")

    @pytest.mark.skip
    @allure.story("Invalid order")
    @allure.title("Cancel with invalid order ID")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_cancel_with_invalid_order_id(self, client):
        """Cancel should handle invalid order IDs gracefully."""
        with allure.step("Send cancel with invalid order ID"):
            invalid_order_id = 9999999999999999999
            result = mt_cancel_order_callback(client, invalid_order_id)
        with allure.step("Validate response"):
            logger.info(f"Invalid order cancel result: {result}")
            assert result is not None

    @pytest.mark.skip
    @allure.story("Duplicate cancel")
    @allure.title("Cancel the same order twice")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cancel_duplicate_order(self, client):
        """Canceling the same order twice should be handled."""
        with allure.step("Create order"):
            result, order_id = mt_push_order_callback(client)
            assert result == "OK", "Push order failed"

        with allure.step("First cancel"):
            result1 = mt_cancel_order_callback(client, order_id)
            logger.info(f"First cancel result: {result1}")
            assert result1 == "OK", f"First cancel failed: {result1}"

        with allure.step("Second cancel"):
            result2 = mt_cancel_order_callback(client, order_id)
            logger.info(f"Second cancel result: {result2}")

        with allure.step("Validate second cancel response"):
            allure.attach(
                str(result2),
                name="duplicate cancel response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert result2 is not None

    @pytest.mark.skip
    @allure.story("Duplicate refund")
    @allure.title("Refund the same order twice")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_refund_duplicate_order(self, client):
        """Refunding the same order twice should be handled."""
        with allure.step("Create order"):
            result, order_id = mt_push_order_callback(client)
            assert result == "OK", "Push order failed"

        with allure.step("First refund"):
            result1 = mt_full_refund_callback(client, order_id)
            logger.info(f"First refund result: {result1}")
            assert result1 == "OK", f"First refund failed: {result1}"

        with allure.step("Second refund"):
            result2 = mt_full_refund_callback(client, order_id)
            logger.info(f"Second refund result: {result2}")

        with allure.step("Validate second refund response"):
            allure.attach(
                str(result2),
                name="duplicate refund response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert result2 is not None

    @pytest.mark.xfail
    @allure.story("Refund after cancel")
    @allure.title("Refund a canceled order")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_refund_cancelled_order(self, client):
        """Refunding a canceled order should be handled."""
        with allure.step("Create order"):
            result, order_id = mt_push_order_callback(client)
            assert result == "OK", "Push order failed"

        with allure.step("Cancel order"):
            cancel_result = mt_cancel_order_callback(client, order_id)
            assert cancel_result == "OK", "Cancel failed"

        with allure.step("Refund canceled order"):
            refund_result = mt_full_refund_callback(client, order_id)
            logger.info(f"Refund canceled order result: {refund_result}")

        with allure.step("Validate refund response"):
            allure.attach(
                str(refund_result),
                name="refund canceled order response",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert refund_result == "ERROR"
