"""
Configure bean of outbound parameters.

Args:
    dir: The directory contains the outbound files.
    ftp: Ftp parameters.
    mq: MQ parameters.
"""

from typing import Optional
from .ftp_config_bean import FtpConfigBean
from .mq_config_bean import MqConfigBean


class InOutConfigBean:
    """
    Configure bean of outbound parameters.
    """
    
    def __init__(self):
        """Initialize the configuration bean with default values."""
        self._name: Optional[str] = None
        self._type: Optional[str] = None
        self._dir: Optional[str] = None
        self._ftp: Optional[FtpConfigBean] = None
        self._mq: Optional[MqConfigBean] = None
    
    @property
    def name(self) -> Optional[str]:
        """Get the identifier of the config segment."""
        return self._name
    
    @name.setter
    def name(self, value: str):
        """Set the identifier of the config segment."""
        self._name = value
    
    @property
    def type(self) -> Optional[str]:
        """Get the data flow type, such as dir to mq."""
        return self._type
    
    @type.setter
    def type(self, value: str):
        """Set the data flow type, such as dir to mq."""
        self._type = value
    
    @property
    def dir(self) -> Optional[str]:
        """Get the directory containing the outbound files."""
        return self._dir
    
    @dir.setter
    def dir(self, value: str):
        """Set the directory containing the outbound files."""
        self._dir = value
    
    @property
    def ftp(self) -> Optional[FtpConfigBean]:
        """Get FTP parameters."""
        return self._ftp
    
    @ftp.setter
    def ftp(self, value: FtpConfigBean):
        """Set FTP parameters."""
        self._ftp = value
    
    @property
    def mq(self) -> Optional[MqConfigBean]:
        """Get MQ parameters."""
        return self._mq
    
    @mq.setter
    def mq(self, value: MqConfigBean):
        """Set MQ parameters."""
        self._mq = value
    
    # 注意：Java 原始代码中有 getMqConfig() 方法，但使用方式不一致
    # 我们保留它作为兼容性方法
    def get_mq_config(self) -> Optional[MqConfigBean]:
        """Get MQ parameters (compatibility method)."""
        return self._mq


# 示例使用代码
if __name__ == "__main__":
    # 创建配置对象
    config = InOutConfigBean()
    
    # 设置属性
    config.name = "OutboundConfig"
    config.type = "dir_to_mq"
    config.dir = "/data/outbound"
    
    # 显示配置
    print(f"Name: {config.name}")
    print(f"Type: {config.type}")
    print(f"Directory: {config.dir}")