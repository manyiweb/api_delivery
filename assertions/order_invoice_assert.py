from typing import Any, Dict, List, Optional


def _to_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _normalize_order_ids(order_ids: Any) -> List[str]:
    if isinstance(order_ids, (list, tuple, set)):
        return [str(item) for item in order_ids]
    return [str(order_ids)]


def assert_basic_response(resp: Dict[str, Any], 接口名称: str) -> None:
    assert isinstance(resp, dict), f"{接口名称}响应不是字典"
    assert str(resp.get("code")) == "200", f"{接口名称}响应码异常: {resp.get('code')}"
    assert resp.get("success") is True, f"{接口名称}返回success异常: {resp.get('success')}"


def assert_apply_response(resp: Dict[str, Any], invoice_id: str, order_ids: Any) -> None:
    assert_basic_response(resp, "开票接口")
    data = resp.get("data")
    assert isinstance(data, dict), "开票接口data不是字典"
    assert str(data.get("invoiceId")) == str(invoice_id), "开票号不一致"

    expected_order_ids = _normalize_order_ids(order_ids)
    response_order_ids = data.get("orderIds")
    if isinstance(response_order_ids, list):
        order_ids_str = [str(item) for item in response_order_ids]
        missing = [order_id for order_id in expected_order_ids if order_id not in order_ids_str]
        assert not missing, f"订单号未出现在开票结果中: {missing}"

    success_count = _to_int(data.get("successCount"))
    if success_count is not None:
        assert success_count >= 1, "开票成功数量异常"

    error_count = _to_int(data.get("errorCount"))
    if error_count is not None:
        assert error_count == 0, "开票错误数量异常"


def assert_refresh_response(resp: Dict[str, Any]) -> None:
    assert_basic_response(resp, "刷新开票状态接口")
    data = resp.get("data")
    if data is not None:
        assert data is True, "刷新接口返回结果异常"


def assert_detail_response(
    resp: Dict[str, Any],
    invoice_id: str,
    order_ids: Any,
    expected_status: str,
) -> None:
    assert_basic_response(resp, "查询开票状态接口")
    data = resp.get("data")
    assert isinstance(data, dict), "开票详情data不是字典"
    assert str(data.get("invoiceId")) == str(invoice_id), "开票号不一致"

    expected_order_ids = _normalize_order_ids(order_ids)

    data_order_id = data.get("orderId")
    if data_order_id is not None:
        assert str(data_order_id) in expected_order_ids, "订单号不一致"

    join_order_list = data.get("joinOrderList")
    if isinstance(join_order_list, list):
        join_order_ids = [
            str(item.get("orderId"))
            for item in join_order_list
            if isinstance(item, dict) and item.get("orderId") is not None
        ]
        if join_order_ids:
            missing = [order_id for order_id in expected_order_ids if order_id not in join_order_ids]
            assert not missing, f"合并订单未全部返回: {missing}"

    status = data.get("status")
    assert str(status) == str(expected_status), "开票状态异常"

    status_desc = data.get("statusDesc")
    if status_desc is not None:
        assert "开票" in str(status_desc), "开票状态描述异常"

    if str(status) == "INVOICED":
        invoice_number = data.get("invoiceNumber") or data.get("invoiceNo")
        assert invoice_number, "开票号码为空"

        invoice_url = data.get("invoiceUrl")
        if invoice_url is not None:
            assert str(invoice_url).strip(), "电子发票地址为空"

        ofd_url = data.get("ofdUrl")
        if ofd_url is not None:
            assert str(ofd_url).strip(), "OFD地址为空"


def assert_red_punch_response(resp: Dict[str, Any]) -> None:
    assert_basic_response(resp, "红冲接口")
    data = resp.get("data")
    assert data is True or str(data).lower() in ("true", "1"), "红冲接口返回结果异常"
