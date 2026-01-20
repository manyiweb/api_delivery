"""日志模块"""
from datetime import datetime
import logging
import os

from config import config

log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), config.LOG_DIR)
os.makedirs(log_dir, exist_ok=True)

log_filename = os.path.join(log_dir, f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger('api_delivery')
logger.info(f"日志文件已创建: {log_filename}")
