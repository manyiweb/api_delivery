from typing import Dict, Any

import httpx

from config import config
from conftest import access_token
from utils.file_loader import load_yaml_data, get_data_file_path




# def build_apply_invoice_payload(order_id: str) -> Dict[str, Any]:


def mgr_apply_invoice(client: httpx.Client, order_id: str) -> Dict[str, Any]:
    invoice_data = load_yaml_data(get_data_file_path("invoice_data.yaml"))
    invoice_data['orderAmountList'][0]['orderId'] = order_id
    invoice_data['orderIds'] = [order_id]
    token = access_token()
    invoice_data['tokenId'] = token

    print(invoice_data)
    apply_invoice_result = client.post(
        url=config.get_base_url() + "/hr/retail/invoice/batchApply",
        json=invoice_data,
        headers={"Authorization": "Bearer " + token},
    )

    return apply_invoice_result.json()


if __name__ == '__main__':
    print(mgr_apply_invoice(httpx.Client(), order_id="f493da2a48fb4e4db552bc492a02fca3"))
