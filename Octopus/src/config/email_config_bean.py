# email_config_bean.py

from typing import List, Optional, TYPE_CHECKING
from .common_config_bean import CommonConfigBean

if TYPE_CHECKING:
    pass

class EmailConfigBean(CommonConfigBean):
    """
    Configure bean of email parameters.
    """
    
    def __init__(self):
        """Initialize the EmailConfigBean with default values."""
        # From CommonConfigBean
        super().__init__()
        
        # EmailConfigBean specific attributes
        self._host: Optional[str] = None
        self._port: int = 23  # Default SMTP port
        self._senders: List[str] = []
        self._receivers: List[str] = []

    def copy(self) -> 'EmailConfigBean':
        """
        Create a copy of this configuration bean.
        
        Returns:
            EmailConfigBean: A new instance with the same properties.
        """
        # Get parent copy
        parent_copy = super().copy()
        
        # Create new instance
        bean = EmailConfigBean()
        
        # Copy parent attributes
        bean._name = parent_copy._name
        bean._id = parent_copy._id
        bean._extend = parent_copy._extend
        bean._mqs = parent_copy._mqs.copy()
        bean._ftps = parent_copy._ftps.copy()
        bean._emails = parent_copy._emails.copy()
        bean._files = parent_copy._files.copy()
        
        # Copy EmailConfigBean specific properties
        bean._host = self._host
        bean._port = self._port
        bean._senders = self._senders.copy()
        bean._receivers = self._receivers.copy()
        
        return bean

    # --- 属性方法 ---

    @property
    def host(self) -> Optional[str]:
        """
        获取邮件主机地址。
        
        返回:
            str: 邮件主机地址。
        """
        return self._host

    @host.setter
    def host(self, value: Optional[str]) -> None:
        """
        设置邮件主机地址。
        
        参数:
            value (str): 邮件主机地址。
        """
        self._host = value

    @property
    def port(self) -> int:
        """
        获取邮件端口。
        
        返回:
            int: 邮件端口。
        """
        return self._port

    @port.setter
    def port(self, value: int) -> None:
        """
        设置邮件端口。
        
        参数:
            value (int): 邮件端口。
        """
        self._port = value

    @property
    def senders(self) -> List[str]:
        """
        获取发送者列表。
        
        返回:
            List[str]: 发送者列表。
        """
        return self._senders

    @senders.setter
    def senders(self, value: List[str]) -> None:
        """
        设置发送者列表。
        
        参数:
            value (List[str]): 发送者列表。
        """
        self._senders = value

    def add_sender(self, sender: str) -> None:
        """
        添加发送者到列表中。
        
        参数:
            sender (str): 发送者邮箱地址。
        """
        self._senders.append(sender)

    @property
    def receivers(self) -> List[str]:
        """
        获取接收者列表。
        
        返回:
            List[str]: 接收者列表。
        """
        return self._receivers

    @receivers.setter
    def receivers(self, value: List[str]) -> None:
        """
        设置接收者列表。
        
        参数:
            value (List[str]): 接收者列表。
        """
        self._receivers = value

    def add_receiver(self, receiver: str) -> None:
        """
        添加接收者到列表中。
        
        参数:
            receiver (str): 接收者邮箱地址。
        """
        self._receivers.append(receiver)

    def __str__(self) -> str:
        """
        返回邮件配置的字符串表示。
        
        返回:
            str: 字符串表示。
        """
        lines = [
            "----------- email config ------------",
            super().__str__()
        ]
        
        for i, sender in enumerate(self._senders):
            lines.append(f"sender {i}\t{sender}")
            
        for i, receiver in enumerate(self._receivers):
            lines.append(f"receiver {i}\t{receiver}")
            
        return "\n".join(lines) + "\n"
    
    # Example usage
if __name__ == "__main__":
    # Test the configuration
    config = EmailConfigBean()
    config.host = "smtp.example.com"
    config.port = 587
    config.add_sender("sender@example.com")
    config.add_receiver("receiver1@example.com")
    config.add_receiver("receiver2@example.com")
    
    print(config)
    
    # Test copy functionality
    config_copy = config.copy()
    print("\nCopied configuration:")
    print(config_copy)