# through_ftp_config_bean.py
"""
Through FTP 配置 Bean 模块

该模块定义了 ThroughFtpConfigBean 类，用于配置通过 FTP 传输的相关参数。
"""

from typing import Optional
from .ftp_config_bean import FtpConfigBean


class ThroughFtpConfigBean:
    """
    Through FTP 参数配置 Bean。
    
    该类用于配置通过 FTP 传输的相关参数，包括是否启用 FTP、大小限制以及 FTP 配置信息。
    """

    def __init__(self):
        """
        使用默认值初始化 ThroughFtpConfigBean 实例。
        """
        # 是否启用 FTP 传输
        self._is_ftp: bool = False
        
        # 传输大小限制（字节）
        self._limited_size: int = 0
        
        # FTP 配置对象
        self._ftp: Optional['FtpConfigBean'] = None

    @property
    def is_ftp(self) -> bool:
        """
        获取 FTP 是否启用的标志。
        
        Returns:
            bool: 如果启用了 FTP 则返回 True，否则返回 False。
        """
        return self._is_ftp

    @is_ftp.setter
    def is_ftp(self, value: bool) -> None:
        """
        设置 FTP 是否启用。
        
        Args:
            value (bool): FTP 启用标志。True 表示启用，False 表示禁用。
        """
        self._is_ftp = value

    @property
    def limited_size(self) -> int:
        """
        获取传输大小限制。
        
        Returns:
            int: 传输大小限制（字节）。
        """
        return self._limited_size

    @limited_size.setter
    def limited_size(self, value: int) -> None:
        """
        设置传输大小限制。
        
        Args:
            value (int): 传输大小限制（字节）。
        """
        self._limited_size = value

    @property
    def ftp(self) -> Optional['FtpConfigBean']:
        """
        获取 FTP 配置对象。
        
        Returns:
            FtpConfigBean: FTP 配置对象，如果未设置则返回 None。
        """
        return self._ftp

    @ftp.setter
    def ftp(self, value: Optional['FtpConfigBean']) -> None:
        """
        设置 FTP 配置对象。
        
        Args:
            value (FtpConfigBean): FTP 配置对象，可以为 None。
        """
        self._ftp = value

    def add_ftp(self, ftp_config: 'FtpConfigBean') -> None:
        """
        添加 FTP 配置。
        
        该方法用于设置 FTP 配置对象，与直接设置 ftp 属性功能相同。
        
        Args:
            ftp_config (FtpConfigBean): 要添加的 FTP 配置对象。
        """
        self._ftp = ftp_config

    def __str__(self) -> str:
        """
        返回对象的字符串表示形式。
        
        Returns:
            str: 对象的字符串表示形式。
        """
        return (f"ThroughFtpConfigBean(is_ftp={self._is_ftp}, "
                f"limited_size={self._limited_size}, "
                f"ftp={'configured' if self._ftp else 'not configured'})")

    def __repr__(self) -> str:
        """
        返回对象的详细字符串表示形式，用于调试。
        
        Returns:
            str: 对象的详细字符串表示形式。
        """
        return (f"ThroughFtpConfigBean(is_ftp={self._is_ftp}, "
                f"limited_size={self._limited_size}, "
                f"ftp={self._ftp!r})")


# 示例用法和测试代码
if __name__ == "__main__":
    # 创建 ThroughFtpConfigBean 实例
    through_ftp_config = ThroughFtpConfigBean()
    
    # 设置属性
    through_ftp_config.is_ftp = True
    through_ftp_config.limited_size = 1024 * 1024  # 1MB
    
    # 输出配置信息
    print("Through FTP 配置:")
    print(f"启用FTP: {through_ftp_config.is_ftp}")
    print(f"大小限制: {through_ftp_config.limited_size} 字节")
    print(f"FTP配置: {through_ftp_config.ftp}")
    
    # 测试字符串表示
    print("\n字符串表示:")
    print(str(through_ftp_config))
    print(repr(through_ftp_config))