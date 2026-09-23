# in_config_bean_pythonic.py
"""
InConfigBean 的 Pythonic 版本
"""

from typing import Optional
from .ftp_config_bean import FtpConfigBean
from .mq_config_bean import MqConfigBean
from .in_out_config_bean import InOutConfigBean

class InConfigBean(InOutConfigBean):
    """
    入站参数配置 Bean。
    
    这个类用于配置入站(inbound)相关的参数，继承自 InOutConfigBean 基类。
    主要包含目录配置以及 FTP 和 MQ 的配置信息。
    """

    def __init__(self):
        """
        初始化 InConfigBean 实例。
        """
        super().__init__()

    def __str__(self) -> str:
        """
        将对象转换为字符串表示形式。
        
        Returns:
            str: 对象的字符串表示。
        """
        buffer = []
        
        # 如果目录存在，则添加到输出中
        if self.dir is not None:
            buffer.append(f"dir : {self.dir}\n")

        # 如果 FTP 配置存在，则添加到输出中
        if self.ftp is not None:
            buffer.append(f"---- ftp ----\n{self.ftp}\n")
            
        # 如果 MQ 配置存在，则添加到输出中
        if self.mq is not None:
            buffer.append(f"---- mq ---\n{self.mq}\n")
            
        return ''.join(buffer)

    @staticmethod
    def main() -> None:
        """
        测试方法。
        """
        pass
