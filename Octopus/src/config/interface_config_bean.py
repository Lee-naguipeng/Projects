"""
Interface configuration bean.
"""

from typing import List, Optional, Any
from .common_config_bean import CommonConfigBean
from .mq_config_bean import MqConfigBean
from .http_config_bean import HttpConfigBean
from .ftp_config_bean import FtpConfigBean
from .email_config_bean import EmailConfigBean
from .file_config_bean import FileConfigBean
from .filter_config_bean import FilterConfigBean


class InterfaceConfigBean(CommonConfigBean):
    """
    Interface configuration bean.
    """
    
    def __init__(self):
        """
        Initialize the interface configuration.
        """
        super().__init__()
        self._private_config: str = ""
        self._private_config_file_name: Optional[str] = None
        self._data_type: Optional[str] = None
        self._transfer_class: Optional[str] = None
        self._type: Optional[str] = None
        self._limited_size: int = -1
        self._content_type: Optional[str] = None
        self._bundle_msgs: bool = False
        self._bundle_keys: Optional[str] = None
        self._bundle_value: Optional[str] = None
        self._bundle_sleep: int = 0
        
        # 初始化各种配置列表
        self._mqs: List[MqConfigBean] = []
        self._https: List[HttpConfigBean] = []
        self._ftps: List[FtpConfigBean] = []
        self._emails: List[EmailConfigBean] = []
        self._files: List[FileConfigBean] = []
        self._filters: List[FilterConfigBean] = []
    
    @property
    def private_config(self) -> str:
        """
        Get private configuration with XML tags.
        """
        return f"<privateConfig>{self._private_config}</privateConfig>"
    
    @private_config.setter
    def private_config(self, value: str):
        """
        Append to private configuration.
        """
        if value is None:
            value = ""
        self._private_config += value
    
    @property
    def private_config_file_name(self) -> Optional[str]:
        """Get private configuration file name."""
        return self._private_config_file_name
    
    @private_config_file_name.setter
    def private_config_file_name(self, value: str):
        """Set private configuration file name."""
        self._private_config_file_name = value
    
    @property
    def data_type(self) -> str:
        """
        Get data type, default to 'plain' if None.
        """
        return self._data_type if self._data_type is not None else "plain"
    
    @data_type.setter
    def data_type(self, value: str):
        """Set data type."""
        self._data_type = value
    
    @property
    def transfer_class(self) -> Optional[str]:
        """Get transfer class."""
        return self._transfer_class
    
    @transfer_class.setter
    def transfer_class(self, value: str):
        """Set transfer class."""
        self._transfer_class = value
    
    @property
    def type(self) -> Optional[str]:
        """Get interface type."""
        return self._type
    
    @type.setter
    def type(self, value: str):
        """Set interface type."""
        self._type = value
    
    @property
    def limited_size(self) -> int:
        """Get limited size (default: -1 for unlimited)."""
        return self._limited_size
    
    @limited_size.setter
    def limited_size(self, value: int):
        """Set limited size."""
        self._limited_size = value
    
    @property
    def content_type(self) -> Optional[str]:
        """Get content type."""
        return self._content_type
    
    @content_type.setter
    def content_type(self, value: str):
        """Set content type."""
        self._content_type = value
    
    @property
    def bundle_msgs(self) -> bool:
        """Get bundle messages flag."""
        return self._bundle_msgs
    
    @bundle_msgs.setter
    def bundle_msgs(self, value: bool):
        """Set bundle messages flag."""
        self._bundle_msgs = value
    
    @property
    def bundle_keys(self) -> str:
        """Get bundle keys, return empty string if None."""
        return self._bundle_keys if self._bundle_keys is not None else ""
    
    @bundle_keys.setter
    def bundle_keys(self, value: str):
        """Set bundle keys."""
        self._bundle_keys = value
    
    @property
    def bundle_value(self) -> str:
        """Get bundle value, return empty string if None."""
        return self._bundle_value if self._bundle_value is not None else ""
    
    @bundle_value.setter
    def bundle_value(self, value: str):
        """Set bundle value."""
        self._bundle_value = value
    
    @property
    def bundle_sleep(self) -> int:
        """Get bundle sleep time."""
        return self._bundle_sleep
    
    @bundle_sleep.setter
    def bundle_sleep(self, value: int):
        """Set bundle sleep time."""
        self._bundle_sleep = value
    
    # MQ configurations
    @property
    def mqs(self) -> List[MqConfigBean]:
        """Get MQ configurations list."""
        return self._mqs
    
    @mqs.setter
    def mqs(self, value: List[MqConfigBean]):
        """Set MQ configurations list."""
        self._mqs = value or []
    
    def add_mq(self, mq: MqConfigBean):
        """Add MQ configuration."""
        if mq is not None:
            self._mqs.append(mq)
    
    # HTTP configurations
    @property
    def https(self) -> List[HttpConfigBean]:
        """Get HTTP configurations list."""
        return self._https
    
    @https.setter
    def https(self, value: List[HttpConfigBean]):
        """Set HTTP configurations list."""
        self._https = value or []
    
    def add_http(self, http: HttpConfigBean):
        """Add HTTP configuration."""
        if http is not None:
            self._https.append(http)
    
    # FTP configurations
    @property
    def ftps(self) -> List[FtpConfigBean]:
        """Get FTP configurations list."""
        return self._ftps
    
    @ftps.setter
    def ftps(self, value: List[FtpConfigBean]):
        """Set FTP configurations list."""
        self._ftps = value or []
    
    def add_ftp(self, ftp: FtpConfigBean):
        """Add FTP configuration."""
        if ftp is not None:
            self._ftps.append(ftp)
    
    # Email configurations
    @property
    def emails(self) -> List[EmailConfigBean]:
        """Get email configurations list."""
        return self._emails
    
    @emails.setter
    def emails(self, value: List[EmailConfigBean]):
        """Set email configurations list."""
        self._emails = value or []
    
    def add_email(self, email: EmailConfigBean):
        """Add email configuration."""
        if email is not None:
            self._emails.append(email)
    
    # File configurations
    @property
    def files(self) -> List[FileConfigBean]:
        """Get file configurations list."""
        return self._files
    
    @files.setter
    def files(self, value: List[FileConfigBean]):
        """Set file configurations list."""
        self._files = value or []
    
    def add_file(self, file: FileConfigBean):
        """Add file configuration."""
        if file is not None:
            self._files.append(file)
    
    # Filter configurations
    @property
    def filters(self) -> List[FilterConfigBean]:
        """Get filter configurations list."""
        return self._filters
    
    @filters.setter
    def filters(self, value: List[FilterConfigBean]):
        """Set filter configurations list."""
        self._filters = value or []
    
    def add_filter(self, filter_: FilterConfigBean):
        """Add filter configuration."""
        if filter_ is not None:
            self._filters.append(filter_)
    
    def do_extend(self, v: List[Any]) -> None:
        """
        Loop on each MQ config, do extend on it; search in v2 first, then search in v.
        
        Args:
            v: Target list to extend with MQ configurations
            
        Raises:
            Exception: If any error occurs during extension
        """
        v.extend(self._mqs)
        
        for mq in self._mqs:
            mq.do_extend(v)
    
    def __str__(self) -> str:
        """
        Get string representation of the interface configuration.
        """
        lines = []
        lines.append("------------- interface config -------------")
        lines.append(f"name->{self.name}")
        lines.append(f"transferClass->{self.transfer_class}")
        lines.append(f"privateConfigFileName->{self.private_config_file_name}")
        lines.append(f"privateConfig->{self._private_config}")
        lines.append(f"limitedSize->{self.limited_size}")
        lines.append(f"contentType->{self.content_type}")
        lines.append(f"bundleMsgs->{self.bundle_msgs}")
        lines.append(f"bundleKeys->{self.bundle_keys}")
        lines.append(f"bundleValue->{self.bundle_value}")
        
        for i, mq in enumerate(self._mqs):
            lines.append(f"------------- mq {i} ------------")
            lines.append(str(mq))
        
        for i, http in enumerate(self._https):
            lines.append(f"------------- http {i} ------------")
            lines.append(str(http))
        
        for i, ftp in enumerate(self._ftps):
            lines.append(f"------------- ftp {i} ------------")
            lines.append(str(ftp))
        
        for i, email in enumerate(self._emails):
            lines.append(f"------------- email {i} ------------")
            lines.append(str(email))
        
        for i, file in enumerate(self._files):
            lines.append(f"------------- file {i} ------------")
            lines.append(str(file))
        
        for i, filter_ in enumerate(self._filters):
            lines.append(f"------------- filter {i} ------------")
            lines.append(str(filter_))
        
        return "\n".join(lines)


# 如果这些引用类不存在，创建简单的占位类
if __name__ == "__main__":
    # 简单的测试
    config = InterfaceConfigBean()
    config.name = "TestInterface"
    config.transfer_class = "com.example.Transfer"
    
    # 设置一些属性
    config.private_config = "Some private config"
    config.limited_size = 1024 * 1024 * 10  # 10MB
    
    # 添加示例配置
    class SimpleMqConfig:
        def __init__(self, name):
            self.name = name
        
        def __str__(self):
            return f"MQ: {self.name}"
    
    config.add_mq(SimpleMqConfig("Queue1"))
    
    print(config)