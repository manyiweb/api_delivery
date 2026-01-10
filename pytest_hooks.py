"""
Pytest配置钩子 - 用于添加Allure环境信息
"""
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
