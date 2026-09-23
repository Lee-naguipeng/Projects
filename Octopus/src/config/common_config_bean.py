# common_config_bean.py
"""
配置 Bean，作为 MQ、Email、FTP 和文件配置的父类。
"""

from typing import List, Optional, Any


class CommonConfigBean:
    """
    配置 Bean，作为各种配置类型的基类。
    
    属性：
        name (str): 配置段的标识符。
        id (str): 配置段的ID。
        extend (str): 扩展信息。
        mqs (List[Any]): MQ 配置列表。
        ftps (List[Any]): FTP 配置列表。
        emails (List[Any]): 邮件配置列表。
        files (List[Any]): 文件配置列表。
    """
    
    def __init__(self,
                 name: Optional[str] = None,
                 id: Optional[str] = None,
                 extend: Optional[str] = None):
        """使用可选值初始化 CommonConfigBean。"""
        self._name = name
        self._id = id
        self._extend = extend
        self._mqs: List[Any] = []
        self._ftps: List[Any] = []
        self._emails: List[Any] = []
        self._files: List[Any] = []

    def copy(self) -> 'CommonConfigBean':
        """
        创建此配置 bean 的副本。
        
        返回:
            CommonConfigBean: 具有相同属性的新实例。
        """
        copy_obj = CommonConfigBean(
            name=self._name,
            id=self._id,
            extend=self._extend
        )
        # 复制集合（浅拷贝）
        copy_obj._mqs = self._mqs.copy()
        copy_obj._ftps = self._ftps.copy()
        copy_obj._emails = self._emails.copy()
        copy_obj._files = self._files.copy()
        return copy_obj

    # --- Name 属性 ---
    @property
    def name(self) -> str:
        """获取配置段的名称。"""
        return self._name if self._name is not None else ""

    @name.setter
    def name(self, value: str) -> None:
        """设置配置段的名称。"""
        self._name = value

    # --- ID 属性 ---
    @property
    def id(self) -> Optional[str]:
        """获取配置段的 ID。"""
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        """设置配置段的 ID。"""
        self._id = value

    # --- Extend 属性 ---
    @property
    def extend(self) -> Optional[str]:
        """获取扩展属性。"""
        return self._extend

    @extend.setter
    def extend(self, value: str) -> None:
        """设置扩展属性。"""
        self._extend = value

    # --- MQs 属性和方法 ---
    @property
    def mqs(self) -> List[Any]:
        """获取 MQ 配置列表。"""
        return self._mqs

    @mqs.setter
    def mqs(self, value: List[Any]) -> None:
        """设置 MQ 配置列表。"""
        self._mqs = value

    def add_mq(self, mq: Any) -> None:
        """向列表中添加 MQ 配置。"""
        self._mqs.append(mq)

    # --- FTPs 属性和方法 ---
    @property
    def ftps(self) -> List[Any]:
        """获取 FTP 配置列表。"""
        return self._ftps

    @ftps.setter
    def ftps(self, value: List[Any]) -> None:
        """设置 FTP 配置列表。"""
        self._ftps = value

    def add_ftp(self, ftp: Any) -> None:
        """向列表中添加 FTP 配置。"""
        self._ftps.append(ftp)

    # --- Emails 属性和方法 ---
    @property
    def emails(self) -> List[Any]:
        """获取邮件配置列表。"""
        return self._emails

    @emails.setter
    def emails(self, value: List[Any]) -> None:
        """设置邮件配置列表。"""
        self._emails = value

    def add_email(self, email: Any) -> None:
        """向列表中添加邮件配置。"""
        self._emails.append(email)

    # --- Files 属性和方法 ---
    @property
    def files(self) -> List[Any]:
        """获取文件配置列表。"""
        return self._files

    @files.setter
    def files(self, value: List[Any]) -> None:
        """设置文件配置列表。"""
        self._files = value

    def add_file(self, file_config: Any) -> None:
        """向列表中添加文件配置。"""
        self._files.append(file_config)

    def __str__(self) -> str:
        """返回配置的字符串表示。"""
        return (f"-------------- common config --------------\n"
                f"name->{self._name}\n"
                f"id->{self._id}\n"
                f"extend->{self._extend}\n")

    def __repr__(self) -> str:
        """返回用于调试的详细表示。"""
        return (f"CommonConfigBean(name={self._name!r}, id={self._id!r}, "
                f"extend={self._extend!r}, mqs_count={len(self._mqs)}, "
                f"ftps_count={len(self._ftps)}, emails_count={len(self._emails)}, "
                f"files_count={len(self._files)})")
    
    # Example usage
if __name__ == "__main__":
    # Create a config instance using Pythonic constructor
    config = CommonConfigBean(name="test_config", id="config_001")
    
    # Use property access (Pythonic way)
    print(config.name)
    config.name = "updated_config"
    
    # Add items to collections
    config.add_mq("mq_config_1")
    config.add_ftp("ftp_config_1")
    
    # Create a copy
    config_copy = config.copy()
    
    print(config)
    print(repr(config))