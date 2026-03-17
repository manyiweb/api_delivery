# -*- coding: utf-8 -*-
"""异步请求工具模块 - 用于高并发场景"""
import asyncio
from typing import Any, Callable, Dict, List, Optional, Tuple

import httpx

from config import config
from utils.logger import logger


async def async_batch_request(
    urls_and_payloads: List[Tuple[str, Dict[str, Any]]],
    method: str = "POST",
    headers: Optional[Dict[str, str]] = None,
    max_concurrency: int = 10,
) -> List[Dict[str, Any]]:
    """
    批量并发请求

    Args:
        urls_and_payloads: [(url, payload), ...] 请求列表
        method: 请求方法
        headers: 请求头
        max_concurrency: 最大并发数

    Returns:
        响应列表（与输入顺序一致）
    """
    semaphore = asyncio.Semaphore(max_concurrency)

    async def _fetch(client: httpx.AsyncClient, url: str, payload: Dict) -> Dict:
        async with semaphore:
            try:
                if method.upper() == "POST":
                    resp = await client.post(url, json=payload)
                else:
                    resp = await client.get(url, params=payload)
                return resp.json()
            except Exception as e:
                logger.error(f"异步请求失败: {url}, 错误: {e}")
                return {"error": str(e)}

    async with httpx.AsyncClient(
        base_url=config.get_base_url(),
        timeout=config.DEFAULT_TIMEOUT,
        headers=headers or {},
    ) as client:
        tasks = [_fetch(client, url, payload)
                 for url, payload in urls_and_payloads]
        return await asyncio.gather(*tasks)


async def async_batch_order_details(
    token_id: str,
    order_ids: List[str],
    max_concurrency: int = 10,
    user_id: str = "f57342198c3147178e5b3ffa63f97a65",
    company_id: str = "5ad586a8721e49518998aedef9fd3b5c",
) -> List[Dict[str, Any]]:
    """
    并发获取多个订单详情

    Args:
        token_id: 访问令牌
        order_ids: 订单ID列表
        max_concurrency: 最大并发数
        user_id: 用户ID
        company_id: 公司ID

    Returns:
        订单详情列表
    """
    semaphore = asyncio.Semaphore(max_concurrency)

    async def _fetch_detail(client: httpx.AsyncClient, order_id: str) -> Dict:
        async with semaphore:
            try:
                payload = {
                    "tokenId": token_id,
                    "orderId": order_id,
                    "userId": user_id,
                    "companyId": company_id,
                }
                resp = await client.post(
                    "/retail-order-front/app/Business/Order/Dock/Detail",
                    json=payload,
                )
                return resp.json()
            except Exception as e:
                logger.error(f"获取订单详情失败: {order_id}, 错误: {e}")
                return {"error": str(e), "orderId": order_id}

    logger.info(f"开始并发获取 {len(order_ids)} 个订单详情，并发数: {max_concurrency}")

    async with httpx.AsyncClient(
        base_url=config.get_base_url(),
        timeout=config.DEFAULT_TIMEOUT,
    ) as client:
        tasks = [_fetch_detail(client, oid) for oid in order_ids]
        results = await asyncio.gather(*tasks)

    logger.info(
        f"并发获取订单详情完成，成功: {len([r for r in results if 'error' not in r])}")
    return results


def run_async(coro):
    """在同步代码中运行异步函数的辅助方法"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 如果已有事件循环在运行，创建新任务
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(coro)
        return loop.run_until_complete(coro)
    except RuntimeError:
        # 没有事件循环时创建新的
        return asyncio.run(coro)


# ============ 便捷的同步包装函数 ============

def batch_order_details(
    token_id: str,
    order_ids: List[str],
    max_concurrency: int = 10,
    user_id: str = "f57342198c3147178e5b3ffa63f97a65",
    company_id: str = "5ad586a8721e49518998aedef9fd3b5c",
) -> List[Dict[str, Any]]:
    """
    同步方式调用并发获取订单详情

    示例:
        results = batch_order_details(token, ["order1", "order2", "order3"])
    """
    return run_async(async_batch_order_details(token_id, order_ids, max_concurrency, user_id, company_id))
