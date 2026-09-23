# -*- coding: utf-8 -*-
"""
CommonHelper - 通用帮助类

包含常量定义和日志工具
"""

import logging
from typing import Optional


class CommonHelper:
    """通用帮助类，包含常量定义和日志工具"""
    
    # 类常量（使用全大写命名）
    BUFFER_SIZE = 512
    
    def __init__(self, logger_name: Optional[str] = None):
        """
        初始化CommonHelper
        
        Args:
            logger_name: 日志器名称，默认为类名
        """
        self._logger = None
        self._logger_name = logger_name or self.__class__.__name__
    
    @property
    def logger(self) -> logging.Logger:
        """
        获取日志器
        
        如果未设置日志器，将创建一个默认的日志器
        
        Returns:
            logging.Logger: 日志器实例
        """
        if self._logger is None:
            # 延迟初始化日志器
            self._logger = self._create_default_logger()
        return self._logger
    
    @logger.setter
    def logger(self, logger_instance: logging.Logger) -> None:
        """
        设置日志器
        
        Args:
            logger_instance: 日志器实例
        """
        if not isinstance(logger_instance, logging.Logger):
            raise TypeError("logger_instance必须是logging.Logger类型")
        self._logger = logger_instance
    
    def _create_default_logger(self) -> logging.Logger:
        """
        创建默认日志器
        
        Returns:
            logging.Logger: 默认日志器实例
        """
        logger = logging.getLogger(self._logger_name)
        
        # 如果没有处理器，添加一个默认的
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        
        return logger
    
    def log_debug(self, message: str, *args, **kwargs) -> None:
        """记录调试日志"""
        self.logger.debug(message, *args, **kwargs)
    
    def log_info(self, message: str, *args, **kwargs) -> None:
        """记录信息日志"""
        self.logger.info(message, *args, **kwargs)
    
    def log_warning(self, message: str, *args, **kwargs) -> None:
        """记录警告日志"""
        self.logger.warning(message, *args, **kwargs)
    
    def log_error(self, message: str, *args, **kwargs) -> None:
        """记录错误日志"""
        self.logger.error(message, *args, **kwargs)
    
    def log_critical(self, message: str, *args, **kwargs) -> None:
        """记录严重错误日志"""
        self.logger.critical(message, *args, **kwargs)
    
    @classmethod
    def get_buffer_size(cls) -> int:
        """
        获取缓冲区大小
        
        Returns:
            int: 缓冲区大小
        """
        return cls.BUFFER_SIZE
    
    @classmethod
    def get_config(cls) -> dict:
        """
        获取配置信息
        
        Returns:
            dict: 配置信息
        """
        return {
            "buffer_size": cls.BUFFER_SIZE,
            "class_name": cls.__name__,
            "module": cls.__module__,
        }


# 模块级别的便捷访问函数
def get_shared_helper() -> CommonHelper:
    """
    获取共享的CommonHelper实例
    
    Returns:
        CommonHelper: 共享实例
    """
    if not hasattr(get_shared_helper, "_shared_instance"):
        get_shared_helper._shared_instance = CommonHelper()
    return get_shared_helper._shared_instance


def log_info(message: str, *args, **kwargs) -> None:
    """便捷函数：记录信息日志"""
    get_shared_helper().log_info(message, *args, **kwargs)


def log_error(message: str, *args, **kwargs) -> None:
    """便捷函数：记录错误日志"""
    get_shared_helper().log_error(message, *args, **kwargs)


# 模块常量（兼容Java的静态访问方式）
BUFFER_SIZE = CommonHelper.BUFFER_SIZE


def main() -> None:
    """
    主函数 - 示例和测试
    
    演示CommonHelper的使用
    """
    # 示例1：使用类的实例
    helper = CommonHelper()
    
    # 记录日志
    helper.log_info("CommonHelper初始化完成")
    helper.log_info(f"缓冲区大小: {helper.get_buffer_size()}")
    
    # 示例2：使用类方法（无需实例化）
    print(f"通过类方法获取缓冲区大小: {CommonHelper.get_buffer_size()}")
    
    # 示例3：获取配置信息
    config = CommonHelper.get_config()
    print(f"配置信息: {config}")
    
    # 示例4：使用便捷函数
    log_info("通过便捷函数记录日志")
    
    # 示例5：自定义日志器
    import sys
    custom_logger = logging.getLogger("CustomLogger")
    custom_handler = logging.StreamHandler(sys.stdout)
    custom_formatter = logging.Formatter('%(levelname)s: %(message)s')
    custom_handler.setFormatter(custom_formatter)
    custom_logger.addHandler(custom_handler)
    custom_logger.setLevel(logging.DEBUG)
    
    helper2 = CommonHelper()
    helper2.logger = custom_logger
    helper2.log_debug("使用自定义日志器")


if __name__ == "__main__":
    # 配置根日志器（用于演示）
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 运行主函数
    main()