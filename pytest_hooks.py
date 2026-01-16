import pytest
import os
from config import config


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config_obj):
    """在pytest配置阶段添加Allure环境信息"""
    # 创建allure-results目录
    allure_dir = config.ALLURE_RESULTS_DIR
    if not os.path.exists(allure_dir):
        os.makedirs(allure_dir)
    
    # 写入环境信息
    env_properties = os.path.join(allure_dir, 'environment.properties')
    with open(env_properties, 'w', encoding='utf-8') as f:
        f.write(f'测试环境={os.getenv("ENV", "test")}\n')
        f.write(f'API地址={config.BASE_URL}\n')
        f.write(f'数据库={config.DB_CONFIG["host"]}:{config.DB_CONFIG["port"]}\n')
        f.write(f'Python版本={os.sys.version}\n')


def pytest_terminal_summary(terminalreporter, exitstatus, config_obj):
    """在终端输出摘要时调用"""
    from utils.notification import NotificationSender, create_test_report_message
    from utils.logger import logger
    
    # 获取测试统计
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    total = passed + failed + skipped
    
    logger.info(f"测试统计: 总数={total}, 通过={passed}, 失败={failed}, 跳过={skipped}")
    
    # 创建通知发送器
    sender = NotificationSender(wechat_webhook=config.WECHAT_WEBHOOK)
    
    # 创建测试报告消息
    content = create_test_report_message(
        passed=passed,
        failed=failed, 
        skipped=skipped,
        total=total
    )
    
    logger.info("正在发送测试结果通知...")
    
    # 发送通知
    results = sender.send_notification(
        content=content,
        title="【自动化测试报告】",
        notification_types=['wechat']
    )
    
    # 检查发送结果
    for ntype, success in results.items():
        if success:
            logger.info(f"✅ {ntype} 通知发送成功")
        else:
            logger.error(f"❌ {ntype} 通知发送失败")
