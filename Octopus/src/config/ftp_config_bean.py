# ftp_config_bean.py
"""
采用Pythonic接口的FTP配置bean。
"""

from typing import List, Optional, Any
from .common_config_bean import CommonConfigBean
from .filter_config_bean import FilterConfigBean

class FtpConfigBean(CommonConfigBean):
    """
    FTP参数配置bean。
    """
    
    def __init__(self):
        """使用默认值初始化FtpConfigBean。"""
        super().__init__()
        
        # FtpConfigBean特定属性
        self._debug: bool = False
        self._filters: Optional[List['FilterConfigBean']] = None
        self._max_connect_attempts: int = 1
        self._connect_attempt_interval: int = 60
        self._quote: Optional[str] = None
        self._is_append: bool = False
        self._is_delete_remote_file: bool = True
        self._local_dir: Optional[str] = None
        self._remote_dir: Optional[str] = None
        self._pattern: Optional[str] = None
        self._mode: Optional[str] = None
        self._ssl_enabled: bool = False
        self._ssh_enabled: bool = False
        self._host: Optional[str] = None
        self._port: int = 21  # 默认FTP端口
        self._account: Optional[str] = None
        self._password: Optional[str] = None
        self._dst_file_name: Optional[str] = None
        self._ori_file_name: Optional[str] = None

    def copy(self) -> 'FtpConfigBean':
        """
        创建此配置bean的副本。
        
        返回:
            FtpConfigBean: 具有相同属性的新实例。
        """
        # 获取父类副本
        parent_copy = super().copy()
        
        # 创建新实例
        bean = FtpConfigBean()
        
        # 复制父类属性
        bean._name = parent_copy._name
        bean._id = parent_copy._id
        bean._extend = parent_copy._extend
        bean._mqs = parent_copy._mqs.copy()
        bean._ftps = parent_copy._ftps.copy()
        bean._emails = parent_copy._emails.copy()
        bean._files = parent_copy._files.copy()
        
        # 复制FTP特定属性
        bean._debug = self._debug
        bean._host = self._host
        bean._password = self._password
        bean._port = self._port
        bean._mode = self._mode
        bean._ssl_enabled = self._ssl_enabled
        bean._ssh_enabled = self._ssh_enabled
        bean._local_dir = self._local_dir
        bean._remote_dir = self._remote_dir
        bean._pattern = self._pattern
        bean._dst_file_name = self._dst_file_name
        bean._is_delete_remote_file = self._is_delete_remote_file
        bean._quote = self._quote
        bean._connect_attempt_interval = self._connect_attempt_interval
        bean._max_connect_attempts = self._max_connect_attempts
        bean._is_append = self._is_append
        bean._ori_file_name = self._ori_file_name
        
        # 深拷贝过滤器列表
        if self._filters:
            bean._filters = [filter.copy() for filter in self._filters]
        
        return bean

    def extend(self, other: 'FtpConfigBean') -> None:
        """
        从另一个FtpConfigBean扩展属性。
        
        参数:
            other (FtpConfigBean): 要从中扩展的FtpConfigBean。
        """
        if other.account is not None:
            self.account = other.account
        if other.dst_file_name is not None:
            self.dst_file_name = other.dst_file_name
        if other.host is not None:
            self.host = other.host
        if not other.is_delete_remote_file:
            self.is_delete_remote_file = False
        if other.local_dir != ".":
            self.local_dir = other.local_dir
        if other.mode != "asc":
            self.mode = other.mode
        if other.password is not None:
            self.password = other.password
        if other.pattern != ".*":
            self.pattern = other.pattern
        if other.ssh_enabled:
            self.ssh_enabled = True
        if self.ssh_enabled and other.port != 22:
            self.port = other.port
        elif not self.ssh_enabled and other.port != 22:
            self.port = other.port
        if other.remote_dir != ".":
            self.remote_dir = other.remote_dir
        if other.quote is not None:
            self.quote = other.quote
        if other.max_connect_attempts != 1:
            self.max_connect_attempts = other.max_connect_attempts
        if other.connect_attempt_interval != 60:
            self.connect_attempt_interval = other.connect_attempt_interval
        self.debug = other.debug

    # --- 属性方法 ---

    @property
    def debug(self) -> bool:
        """获取调试标志。"""
        return self._debug

    @debug.setter
    def debug(self, value: bool) -> None:
        """设置调试标志。"""
        self._debug = value

    @property
    def filters(self) -> Optional[List['FilterConfigBean']]:
        """获取过滤器列表。"""
        return self._filters

    @filters.setter
    def filters(self, value: Optional[List['FilterConfigBean']]) -> None:
        """设置过滤器列表。"""
        self._filters = value

    def add_filter(self, filter_bean: 'FilterConfigBean') -> None:
        """向列表中添加过滤器。"""
        if self._filters is None:
            self._filters = []
        self._filters.append(filter_bean)

    @property
    def max_connect_attempts(self) -> int:
        """获取最大连接尝试次数。"""
        return self._max_connect_attempts

    @max_connect_attempts.setter
    def max_connect_attempts(self, value: int) -> None:
        """设置最大连接尝试次数。"""
        self._max_connect_attempts = value

    @property
    def connect_attempt_interval(self) -> int:
        """获取连接尝试间隔。"""
        return self._connect_attempt_interval

    @connect_attempt_interval.setter
    def connect_attempt_interval(self, value: int) -> None:
        """设置连接尝试间隔。"""
        self._connect_attempt_interval = value

    @property
    def quote(self) -> Optional[str]:
        """获取引号。"""
        return self._quote

    @quote.setter
    def quote(self, value: Optional[str]) -> None:
        """设置引号。"""
        self._quote = value

    @property
    def is_append(self) -> bool:
        """获取是否追加。"""
        return self._is_append

    @is_append.setter
    def is_append(self, value: bool) -> None:
        """设置是否追加。"""
        self._is_append = value

    @property
    def is_delete_remote_file(self) -> bool:
        """获取是否删除远程文件。"""
        return self._is_delete_remote_file

    @is_delete_remote_file.setter
    def is_delete_remote_file(self, value: bool) -> None:
        """设置是否删除远程文件。"""
        self._is_delete_remote_file = value

    @property
    def local_dir(self) -> str:
        """获取本地目录。"""
        return self._local_dir if self._local_dir is not None else "."

    @local_dir.setter
    def local_dir(self, value: Optional[str]) -> None:
        """设置本地目录。"""
        self._local_dir = value

    @property
    def remote_dir(self) -> str:
        """获取远程目录。"""
        return self._remote_dir if self._remote_dir is not None else "."

    @remote_dir.setter
    def remote_dir(self, value: Optional[str]) -> None:
        """设置远程目录。"""
        self._remote_dir = value

    @property
    def pattern(self) -> str:
        """获取模式。"""
        return self._pattern if self._pattern is not None else ".*"

    @pattern.setter
    def pattern(self, value: Optional[str]) -> None:
        """设置模式。"""
        self._pattern = value

    @property
    def mode(self) -> str:
        """获取传输模式。"""
        if self._mode is None:
            return "asc"
        if self._mode.lower() in ("asc", "ascii"):
            return "asc"
        if self._mode.lower() == "bin":
            return "bin"
        return "asc"

    @mode.setter
    def mode(self, value: Optional[str]) -> None:
        """设置传输模式。"""
        self._mode = value

    @property
    def ssl_enabled(self) -> bool:
        """获取SSL是否启用。"""
        return self._ssl_enabled

    @ssl_enabled.setter
    def ssl_enabled(self, value: bool) -> None:
        """设置SSL是否启用。"""
        self._ssl_enabled = value

    @property
    def ssh_enabled(self) -> bool:
        """获取SSH是否启用。"""
        return self._ssh_enabled

    @ssh_enabled.setter
    def ssh_enabled(self, value: bool) -> None:
        """设置SSH是否启用。"""
        self._ssh_enabled = value

    @property
    def host(self) -> Optional[str]:
        """获取FTP主机。"""
        return self._host

    @host.setter
    def host(self, value: Optional[str]) -> None:
        """设置FTP主机。"""
        self._host = value

    @property
    def port(self) -> int:
        """获取FTP端口。"""
        return 22 if self.ssh_enabled else self._port

    @port.setter
    def port(self, value: int) -> None:
        """设置FTP端口。"""
        self._port = value

    @property
    def account(self) -> Optional[str]:
        """获取FTP账户。"""
        return self._account

    @account.setter
    def account(self, value: Optional[str]) -> None:
        """设置FTP账户。"""
        self._account = value

    @property
    def password(self) -> Optional[str]:
        """获取FTP密码。"""
        return self._password

    @password.setter
    def password(self, value: Optional[str]) -> None:
        """设置FTP密码。"""
        self._password = value

    @property
    def dst_file_name(self) -> Optional[str]:
        """获取目标文件名。"""
        return self._dst_file_name

    @dst_file_name.setter
    def dst_file_name(self, value: Optional[str]) -> None:
        """设置目标文件名。"""
        self._dst_file_name = value

    @property
    def ori_file_name(self) -> Optional[str]:
        """获取原始文件名。"""
        return self._ori_file_name

    @ori_file_name.setter
    def ori_file_name(self, value: Optional[str]) -> None:
        """设置原始文件名。"""
        self._ori_file_name = value

    def __str__(self) -> str:
        """
        返回FTP配置的字符串表示。
        
        返回:
            str: 字符串表示。
        """
        lines = [
            "-------------- ftp config --------------",
            super().__str__(),
            f"host : {self._host}",
            f"port : {self.port}",
            f"account : {self._account}",
            f"password : {self._password}",
            f"dst_file_name : {self._dst_file_name}",
            f"is_append : {self._is_append}",
            f"quote : {self._quote}",
            f"is_delete_remote_file : {self._is_delete_remote_file}",
            f"ssh_enabled : {self._ssh_enabled}",
            f"ssl_enabled : {self._ssl_enabled}",
            f"connect_attempt_interval : {self._connect_attempt_interval}",
            f"max_connect_attempts : {self._max_connect_attempts}",
            f"debug : {self._debug}"
        ]
        
        if self.mqs:
            for mq in self.mqs:
                lines.append(str(mq))
                
        if self.filters:
            for filter_bean in self.filters:
                lines.append(str(filter_bean))
                
        return "\n".join(lines) + "\n"

# Example usage and testing
if __name__ == "__main__":
   ftp_config=FtpConfigBean()  
   ftp_config.mqs =[CommonConfigBean()]
   ftp_config.filters=[FilterConfigBean()]

   print (ftp_config)