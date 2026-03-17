import os
from typing import Any, Dict, Optional

import yaml

from utils.logger import logger


def load_yaml_data(file_path: str) -> Optional[Dict[str, Any]]:
    """从 YAML 文件加载数据。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"YAML 文件未找到: {file_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"YAML 解析失败: {file_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"加载 YAML 失败: {file_path}: {e}")
        raise


def get_data_file_path(filename: str) -> str:
    """获取 data 目录下的文件路径。"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, 'data', filename)
