# tp_config_bean_pythonic.py
"""
TPConfigBean 的 Pythonic 版本
"""

from typing import List, Optional, Any
from pathlib import Path
from .common_thread_bean import CommonThreadBean
from .mq_config_bean import MqConfigBean
from .ftp_config_bean import FtpConfigBean
from .email_config_bean import EmailConfigBean
from .file_config_bean import FileConfigBean
from .interface_config_bean import InterfaceConfigBean
from .in_config_bean import InConfigBean
from .out_config_bean import OutConfigBean


class TPConfigBean(CommonThreadBean):
    """
    交易伙伴配置 Bean。
    
    这个类用于配置消息参数，包含各种通信方式的配置，
    如 MQ、FTP、邮件、文件等，以及接口和输入输出配置。
    """

    def __init__(self):
        """
        初始化 TPConfigBean 实例。
        """
        super().__init__()
        # 各种配置列表
        self._mqs: Optional[List['MqConfigBean']] = None
        self._ftps: Optional[List['FtpConfigBean']] = None
        self._emails: Optional[List['EmailConfigBean']] = None
        self._files: Optional[List['FileConfigBean']] = None
        self._interfaces: Optional[List['InterfaceConfigBean']] = None
        
        # 标志和配置属性
        self._is_stand_alone: bool = False
        self._process_type: str = "ALL"
        self._class_name: Optional[str] = None
        self._controller_name: Optional[str] = None
        
        # 输入输出配置
        self._in_config: Optional['InConfigBean'] = None
        self._out_config: Optional['OutConfigBean'] = None

    # MQ 配置属性
    @property
    def mqs(self) -> Optional[List['MqConfigBean']]:
        """
        获取 MQ 配置列表。
        
        Returns:
            List[MqConfigBean]: MQ 配置列表。
        """
        return self._mqs

    @mqs.setter
    def mqs(self, value: Optional[List['MqConfigBean']]) -> None:
        """
        设置 MQ 配置列表。
        
        Args:
            value (List[MqConfigBean]): MQ 配置列表。
        """
        self._mqs = value

    def add_mq(self, mq: 'MqConfigBean') -> None:
        """
        添加 MQ 配置到列表中。
        
        Args:
            mq (MqConfigBean): 要添加的 MQ 配置。
        """
        if self._mqs is None:
            self._mqs = []
        self._mqs.append(mq)

    # FTP 配置属性
    @property
    def ftps(self) -> Optional[List['FtpConfigBean']]:
        """
        获取 FTP 配置列表。
        
        Returns:
            List[FtpConfigBean]: FTP 配置列表。
        """
        return self._ftps

    @ftps.setter
    def ftps(self, value: Optional[List['FtpConfigBean']]) -> None:
        """
        设置 FTP 配置列表。
        
        Args:
            value (List[FtpConfigBean]): FTP 配置列表。
        """
        self._ftps = value

    def add_ftp(self, ftp: 'FtpConfigBean') -> None:
        """
        添加 FTP 配置到列表中。
        
        Args:
            ftp (FtpConfigBean): 要添加的 FTP 配置。
        """
        if self._ftps is None:
            self._ftps = []
        self._ftps.append(ftp)

    # 邮件配置属性
    @property
    def emails(self) -> Optional[List['EmailConfigBean']]:
        """
        获取邮件配置列表。
        
        Returns:
            List[EmailConfigBean]: 邮件配置列表。
        """
        return self._emails

    @emails.setter
    def emails(self, value: Optional[List['EmailConfigBean']]) -> None:
        """
        设置邮件配置列表。
        
        Args:
            value (List[EmailConfigBean]): 邮件配置列表。
        """
        self._emails = value

    def add_email(self, email: 'EmailConfigBean') -> None:
        """
        添加邮件配置到列表中。
        
        Args:
            email (EmailConfigBean): 要添加的邮件配置。
        """
        if self._emails is None:
            self._emails = []
        self._emails.append(email)

    # 文件配置属性
    @property
    def files(self) -> Optional[List['FileConfigBean']]:
        """
        获取文件配置列表。
        
        Returns:
            List[FileConfigBean]: 文件配置列表。
        """
        return self._files

    @files.setter
    def files(self, value: Optional[List['FileConfigBean']]) -> None:
        """
        设置文件配置列表。
        
        Args:
            value (List[FileConfigBean]): 文件配置列表。
        """
        self._files = value

    def add_file(self, file_config: 'FileConfigBean') -> None:
        """
        添加文件配置到列表中。
        
        Args:
            file_config (FileConfigBean): 要添加的文件配置。
        """
        if self._files is None:
            self._files = []
        self._files.append(file_config)

    # 接口配置属性
    @property
    def interfaces(self) -> Optional[List['InterfaceConfigBean']]:
        """
        获取接口配置列表。
        
        Returns:
            List[InterfaceConfigBean]: 接口配置列表。
        """
        return self._interfaces

    @interfaces.setter
    def interfaces(self, value: Optional[List['InterfaceConfigBean']]) -> None:
        """
        设置接口配置列表。
        
        Args:
            value (List[InterfaceConfigBean]): 接口配置列表。
        """
        self._interfaces = value

    def add_interface(self, interface: 'InterfaceConfigBean') -> None:
        """
        添加接口配置到列表中。
        
        Args:
            interface (InterfaceConfigBean): 要添加的接口配置。
        """
        if self._interfaces is None:
            self._interfaces = []
        self._interfaces.append(interface)

    def do_extend(self, config_list: List[Any]) -> None:
        """
        执行扩展操作。
        
        首先对 'mqs' 执行扩展；然后对每个接口执行扩展。
        
        Args:
            config_list: 要搜索的父级配置列表。
        """
        config_list.append(self.mqs)
        
        if self.mqs is not None:
            for mq in self.mqs:
                mq.do_extend(config_list)
                
        if self.interfaces is not None:
            for interface in self.interfaces:
                interface.do_extend(config_list)

    def copy(self, name: str) -> 'TPConfigBean':
        """
        复制当前配置到新对象。
        
        Args:
            name (str): 新配置的名称。
            
        Returns:
            TPConfigBean: 新的配置对象。
        """
        new_config = TPConfigBean()
        
        # 复制 CommonThreadBean 的属性
        new_config.private_config_file_name = self.private_config_file_name
        new_config.alive_msg = self.alive_msg
        new_config.app_trace_flag = self.app_trace_flag
        new_config.error_msg = self.error_msg
        new_config.is_send_alive = self.is_send_alive
        new_config.is_send_error = self.is_send_error
        new_config.log_dir = self.log_dir
        new_config.log_level = self.log_level
        new_config.log_retention = self.log_retention
        new_config.mq_trace_flag = self.mq_trace_flag
        new_config.name = name  # 重命名新对象
        new_config.run_flag = self.run_flag
        new_config.run_type = self.run_type
        new_config.sleep_time = self.sleep_time
        
        # 复制自身属性
        new_config.is_stand_alone = self.is_stand_alone
        new_config.process_type = self.process_type
        new_config.class_name = self.class_name
        new_config.controller_name = self.controller_name
        new_config.in_config = self.in_config
        new_config.out_config = self.out_config
        new_config.emails = self.emails
        new_config.files = self.files
        new_config.ftps = self.ftps
        new_config.interfaces = self.interfaces
        
        return new_config

    # 独立运行标志属性
    @property
    def is_stand_alone(self) -> bool:
        """
        获取是否独立运行标志。
        
        Returns:
            bool: 独立运行标志。
        """
        return self._is_stand_alone

    @is_stand_alone.setter
    def is_stand_alone(self, value: bool) -> None:
        """
        设置是否独立运行标志。
        
        Args:
            value (bool): 独立运行标志。
        """
        self._is_stand_alone = value

    # 处理类型属性
    @property
    def process_type(self) -> str:
        """
        获取处理类型。
        
        Returns:
            str: 处理类型。
        """
        return self._process_type

    @process_type.setter
    def process_type(self, value: str) -> None:
        """
        设置处理类型。
        
        Args:
            value (str): 处理类型。
        """
        self._process_type = value

    # 类名属性
    @property
    def class_name(self) -> str:
        """
        获取实现类名。
        
        Returns:
            str: 实现类名。
        """
        if self._class_name is not None and self._class_name.strip():
            return self._class_name
        else:
            return "com.ibm.dsg.cr20050098.CommonTP"

    @class_name.setter
    def class_name(self, value: Optional[str]) -> None:
        """
        设置实现类名。
        
        Args:
            value (str): 实现类名。
        """
        self._class_name = value

    # 控制器名称属性
    @property
    def controller_name(self) -> Optional[str]:
        """
        获取控制器名称。
        
        Returns:
            str: 控制器名称。
        """
        return self._controller_name

    @controller_name.setter
    def controller_name(self, value: Optional[str]) -> None:
        """
        设置控制器名称。
        
        Args:
            value (str): 控制器名称。
        """
        self._controller_name = value

    # 输入配置属性
    @property
    def in_config(self) -> Optional['InConfigBean']:
        """
        获取输入配置。
        
        Returns:
            InConfigBean: 输入配置。
        """
        return self._in_config

    @in_config.setter
    def in_config(self, value: Optional['InConfigBean']) -> None:
        """
        设置输入配置。
        
        Args:
            value (InConfigBean): 输入配置。
        """
        self._in_config = value

    # 输出配置属性
    @property
    def out_config(self) -> Optional['OutConfigBean']:
        """
        获取输出配置。
        
        Returns:
            OutConfigBean: 输出配置。
        """
        return self._out_config

    @out_config.setter
    def out_config(self, value: Optional['OutConfigBean']) -> None:
        """
        设置输出配置。
        
        Args:
            value (OutConfigBean): 输出配置。
        """
        self._out_config = value

    def __str__(self) -> str:
        """
        将对象转换为字符串表示。
        
        Returns:
            str: 对象的字符串表示。
        """
        buffer = [super().__str__()]
        buffer.append(f"standAlone : {self.is_stand_alone}\n")
        buffer.append(f"processType : {self.process_type}\n")
        buffer.append(f"class : {self.class_name}\n")
        
        if self.mqs is not None:
            for i, mq in enumerate(self.mqs):
                buffer.append(f"---- mq {i} ----\n")
                buffer.append(str(mq))
                
        if self.interfaces is not None:
            for i, interface in enumerate(self.interfaces):
                buffer.append(f"---- interface {i} ----\n")
                buffer.append(str(interface))
                
        return ''.join(buffer)

    @staticmethod
    def main() -> None:
        """
        测试所有方法。
        """
        pass


# 测试代码
if __name__ == "__main__":
    # 创建 TPConfigBean 实例
    tp_config = TPConfigBean()
    
    # 设置基本属性
    tp_config.name = "TestPartner"
    tp_config.is_stand_alone = True
    tp_config.process_type = "IN"
    tp_config.class_name = "com.example.CustomTP"
    tp_config.controller_name = "MainController"
    
    # 输出配置信息
    print("TPConfigBean 实例:")
    print(tp_config)
    
    # 测试复制功能
    copied_config = tp_config.copy("CopiedPartner")
    print("\n复制的配置:")
    print(copied_config)