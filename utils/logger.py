from datetime import datetime
import logging
import os

# 创建 logs 目录
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 生成带时间戳的日志文件名
log_filename = os.path.join(log_dir, f'test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),  # 输出到文件
            logging.StreamHandler()  # 同时输出到控制台
    ]
)

# 创建全局logger
logger = logging.getLogger('api_delivery')
logger.info(f"日志文件已创建: {log_filename}")
