import json
import time
import allure

from utils.file_loader import get_data_file_path, load_yaml_data
from utils.logger import logger


# 构建美团推单接口参数
def build_final_payload(raw_data, order_id=None):
    """
    根据美团接口要求，执行多层 JSON 序列化，并构建最终的请求 payload。

    注意：使用 separators=(',', ':') 保证输出的 JSON 字符串是紧凑的，
          避免因空格导致的签名校验失败。
    """
    if not raw_data:
        return None

    # --- 1. 动态生成唯一ID，防止订单重复 ---
    timestamp_part = int((time.time() * 1000))  # 标准美团订单号 5301890193521352344
    if order_id is None:
        order_id = int('5301890196' + str(timestamp_part)[-9:])  # 模拟生成唯一订单ID

    # --- 2. 处理 poiReceiveDetail 内部的 JSON 字符串 (reconciliationExtras) ---
    reconciliation_extras_str = json.dumps(
        raw_data['reconciliation_extras'],
        ensure_ascii=False,
        separators=(',', ':')
    )

    # 将字符串赋值给 poi_receive_detail
    poi_receive_detail = raw_data['poi_receive_detail']
    poi_receive_detail['reconciliationExtras'] = reconciliation_extras_str

    # --- 3. 构建 order_dict ---
    order_dict = raw_data['order_core_params']

    # 覆盖动态字段
    order_dict['ctime'] = timestamp_part
    order_dict['utime'] = timestamp_part
    order_dict['orderId'] = order_id
    order_dict['orderIdView'] = order_id

    # 对嵌套的复杂结构进行序列化
    order_dict['detail'] = json.dumps(
        raw_data['detail_list'],
        ensure_ascii=False,
        separators=(',', ':')
    )
    order_dict['extras'] = json.dumps(
        raw_data['extras_list'],
        ensure_ascii=False,
        separators=(',', ':')
    )
    order_dict['poiReceiveDetail'] = json.dumps(
        poi_receive_detail,
        ensure_ascii=False,
        separators=(',', ':')
    )

    # --- 4. 构建最终 payload ---
    final_payload = raw_data['final_payload_params'].copy()
    # print(final_payload)
    # 序列化整个 order_dict 作为 'order' 参数的值
    final_payload['order'] = json.dumps(
        order_dict,
        ensure_ascii=False,
        separators=(',', ':')
    )

    return final_payload, order_id


# 构建美团取消订单接口参数
def build_cancel_payload(raw_data, order_id):
    """
    根据美团接口要求，执行多层 JSON 序列化，并构建最终的请求 payload。

    注意：使用 separators=(',', ':') 保证输出的 JSON 字符串是紧凑的，
          避免因空格导致的签名校验失败。
    """

    print("当前要取消的订单ID:", order_id)
    if not raw_data:
        return None

    cancelOrder_list = raw_data['orderCancel_list'].copy()
    logger.debug(f"取消订单列表: {cancelOrder_list}")
    # 替换新生成的订单ID
    cancelOrder_list['orderId'] = order_id
    # 序列化整个 cancelOrder_list 去除空格 ,
    cancelOrder_list = json.dumps(
        cancelOrder_list,
        ensure_ascii=False,
        separators=(',', ':')
    )
    logger.debug(f"序列化后的取消订单列表: {cancelOrder_list}")

    # 构建最终参数
    cancel_payload = raw_data['final_cancelOrder_params'].copy()
    cancel_payload['orderCancel'] = cancelOrder_list
    logger.info(f"取消订单最终参数: {cancel_payload}")

    return cancel_payload


# 构建申请订单整单退接口参数
def build_apply_refund_payload(raw_data,order_id):
    """
    根据美团接口要求，执行多层 JSON 序列化，并构建最终的请求 payload。

    注意：使用 separators=(',', ':') 保证输出的 JSON 字符串是紧凑的，
          避免因空格导致的签名校验失败。
    """
    if not raw_data:
        return None

    # 序列化 orderRefund_list 参数
    orderRefund_list = raw_data['orderRefund_list'].copy()
    orderRefund_list['orderId'] = order_id
    orderRefund_list = json.dumps(
        orderRefund_list,
        ensure_ascii=False,
        separators=(',', ':')
    )

    allure.attach(json.dumps(raw_data, ensure_ascii=False, indent=2),
                  name="申请订单整单退原始参数", attachment_type=allure.attachment_type.JSON)
    final_applyOrder_params = raw_data['final_applyOrder_params'].copy()
    final_applyOrder_params['orderRefund'] = orderRefund_list
    final_payload = final_applyOrder_params
    return final_payload


if __name__ == '__main__':
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(current_dir, 'data', 'delivery_data.yaml')
    # raw_data = load_yaml_data(file_path)
    # final_payload, order_id = build_final_payload(raw_data)
    # print('生成的订单ID为:', order_id)
    # print('final_payload', final_payload)
    #
    # print(get_data_file_path('cancel_order.yaml'))

    # 调试取消订单接口
    # raw_data2 = load_yaml_data(get_data_file_path('cancel_order.yaml'))
    # print('raw_data2', raw_data2)
    # cancel_payload = build_cancel_payload(raw_data2, 530189019046131710)
    #
    # with httpx.Client(base_url=BASE_URL) as client:
    #     responses = safe_post(client, '/mt/v2/order/cancel/callback', data=cancel_payload)
    #     resp = responses.json().get('data')
    #     print('取消订单响应:', resp)
    raw_data = load_yaml_data(get_data_file_path('refund_order.yaml'))
    print(build_apply_refund_payload(raw_data))
