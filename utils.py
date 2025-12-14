import time
import yaml
import os
import json


# 读取delivery_data.yaml数据
def load_yaml_data(file_path):
    """从 YAML 文件中加载原始配置数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: YAML file not found at {file_path}")
        return None


def get_data_file_path(filename):
    """获取 data 目录下的文件路径"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(project_root, 'data', filename)


# 构建美团推单接口参数
def build_final_payload(raw_data):
    """
    根据美团接口要求，执行多层 JSON 序列化，并构建最终的请求 payload。

    注意：使用 separators=(',', ':') 保证输出的 JSON 字符串是紧凑的，
          避免因空格导致的签名校验失败。
    """
    if not raw_data:
        return None

    # --- 1. 动态生成唯一ID，防止订单重复 ---
    timestamp_part = int((time.time() * 1000))  # 标准美团订单号 5301890193521352344
    print("当前时间戳后9位:", timestamp_part)
    order_id = int('530189019' + str(timestamp_part)[-9:])  # 模拟生成唯一订单ID

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
    print(final_payload)
    # 序列化整个 order_dict 作为 'order' 参数的值
    final_payload['order'] = json.dumps(
        order_dict,
        ensure_ascii=False,
        separators=(',', ':')
    )

    return final_payload, order_id

# 构建美团取消订单接口参数
def build_cancel_payload(raw_data):
    """
    根据美团接口要求，执行多层 JSON 序列化，并构建最终的请求 payload。

    注意：使用 separators=(',', ':') 保证输出的 JSON 字符串是紧凑的，
          避免因空格导致的签名校验失败。
    """
    if not raw_data:
        return None



if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data', 'delivery_data.yaml')
    raw_data = load_yaml_data(file_path)
    final_payload, order_id = build_final_payload(raw_data)
    print(final_payload)

    print(get_data_file_path('cancel_order.yaml'))
