# Author：zww
# Date ：2026/3/27 11:03
# DESCRIPTION：.log装饰器

import functools
import time
from typing import Callable

# 从当前包中导入 LoggerManager，用于获取日志记录器实例以输出运行和调试信息
from agents.common.utils.logger import LoggerManager
# 获取全局日志实例，用于在工具加载和调用过程中记录日志
logger = LoggerManager.get_logger()

# 结点日志装饰器
def log_node():

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 获取logger
            node_name = func.__name__

            # 记录开始
            logger.info(f"[{node_name}] Started with args: {args}, kwargs: {kwargs}")
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                logger.info(f"[{node_name}] Completed in {elapsed:.2f}s")
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(
                    f"[{node_name}] Failed after {elapsed:.2f}s: {e}",
                    exc_info=True
                )
                raise

        return wrapper

    return decorator


