from typing import Any, Dict, Optional

from utils.allure_helper import attach_json, attach_text


def _response_json(response: Any) -> Dict[str, Any]:
    payload = response.json()
    assert isinstance(payload, dict), f"支付响应不是字典: {payload!r}"
    return payload


def _business_code(payload: Dict[str, Any]) -> Optional[str]:
    code = payload.get("code", payload.get("ResultInt"))
    return None if code is None else str(code)


def _is_business_success(payload: Dict[str, Any]) -> bool:
    code = _business_code(payload)
    success = payload.get("success")
    if success is False:
        return False
    if code in {"200", "0"}:
        return success is not False
    if success is True and code is None:
        return True
    return False


def _extract_order_id(payload: Dict[str, Any]) -> Optional[str]:
    data = payload.get("data")
    if isinstance(data, dict):
        order_id = data.get("orderId") or data.get("order_id")
        if order_id:
            return str(order_id)

    for key in ("orderId", "order_id", "OrderId"):
        order_id = payload.get(key)
        if order_id:
            return str(order_id)

    return None


def assert_pay_success(response: Any, scene: str, *, order_id: Optional[str] = None) -> Dict[str, Any]:
    """Assert HTTP and business success for payment-like APIs."""
    status_code = getattr(response, "status_code", None)
    if status_code is not None:
        assert status_code == 200, f"{scene} HTTP 状态码异常: {status_code}"

    payload = _response_json(response)
    attach_json(f"{scene}响应摘要", payload)

    code = _business_code(payload)
    message = payload.get("msg") or payload.get("message") or payload.get("ResultString") or ""
    assert _is_business_success(payload), f"{scene}业务结果异常: code={code}, msg={message}"

    if order_id is not None:
        actual_order_id = _extract_order_id(payload)
        if actual_order_id is not None:
            assert actual_order_id == str(order_id), (
                f"{scene}订单号不一致: 期望 {order_id}, 实际 {actual_order_id}"
            )
        attach_text(f"{scene}订单号", order_id)

    return payload
