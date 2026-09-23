# tps_config_bean_pythonic.py
"""
TPsConfigBean 的 Pythonic 版本
"""

import os
from typing import List, Optional
from pathlib import Path
from .common_thread_bean import CommonThreadBean
from .tp_config_bean import TPConfigBean
from .controller_config_bean import ControllerConfigBean
from .mq_config_bean import MqConfigBean


class TPsConfigBean(CommonThreadBean):
    """
    消息参数配置 Bean。
    
    与 CommonConfigBean 相比，TPsConfigBean 提供了更高级别的配置管理，
    包括工作目录、日志目录、备份目录、临时目录以及合作伙伴、控制器和MQ配置的集合。
    """

    def __init__(self):
        """
        初始化 TPsConfigBean 实例。
        """
        super().__init__()
        self._work_dir: Optional[str] = None
        self._log_dir: Optional[str] = None
        self._backup_dir: Optional[str] = None
        self._tmp_dir: Optional[str] = None
        self._partners: List['TPConfigBean'] = []
        self._controllers: List['ControllerConfigBean'] = []
        self._mqs: List['MqConfigBean'] = []

    # 工作目录属性
    @property
    def work_dir(self) -> Optional[str]:
        """
        获取工作目录路径。
        
        如果未设置，尝试从 OCTOPUS_HOME 环境变量获取。
        
        Returns:
            str: 工作目录路径。
        """
        if self._work_dir is None:
            self._work_dir = os.environ.get("OCTOPUS_HOME")
        return self._work_dir

    @work_dir.setter
    def work_dir(self, value: str) -> None:
        """
        设置工作目录路径。
        
        Args:
            value (str): 工作目录路径。
        """
        self._work_dir = value

    # 日志目录属性
    @property
    def log_dir(self) -> Optional[str]:
        """
        获取日志目录路径。
        
        Returns:
            str: 日志目录路径。
        """
        return self._log_dir

    @log_dir.setter
    def log_dir(self, value: str) -> None:
        """
        设置日志目录路径。
        
        Args:
            value (str): 日志目录路径。
        """
        if not value.strip():
            if self.work_dir:
                self._log_dir = os.path.join(self.work_dir, "log")
            return

        if value.startswith((os.sep, '/')):
            self._log_dir = value
        elif self.work_dir:
            self._log_dir = os.path.join(self.work_dir, value)
        else:
            self._log_dir = os.path.join(os.sep, value)

    # 备份目录属性
    @property
    def backup_dir(self) -> Optional[str]:
        """
        获取备份目录路径。
        
        Returns:
            str: 备份目录路径。
        """
        return self._backup_dir

    @backup_dir.setter
    def backup_dir(self, value: str) -> None:
        """
        设置备份目录路径。
        
        Args:
            value (str): 备份目录路径。
        """
        if not value.strip():
            if self.work_dir:
                self._backup_dir = os.path.join(self.work_dir, "backup")
            return

        if value.startswith((os.sep, '/')):
            self._backup_dir = value
        elif self.work_dir:
            self._backup_dir = os.path.join(self.work_dir, value)
        else:
            self._backup_dir = os.path.join(os.sep, value)

    # 临时目录属性
    @property
    def tmp_dir(self) -> Optional[str]:
        """
        获取临时目录路径。
        
        Returns:
            str: 临时目录路径。
        """
        return self._tmp_dir

    @tmp_dir.setter
    def tmp_dir(self, value: str) -> None:
        """
        设置临时目录路径。
        
        Args:
            value (str): 临时目录路径。
        """
        if not value.strip():
            if self.work_dir:
                self._tmp_dir = os.path.join(self.work_dir, "tmp")
            return

        if value.startswith(os.sep):
            self._tmp_dir = value
        elif self.work_dir:
            self._tmp_dir = os.path.join(self.work_dir, value)
        else:
            self._tmp_dir = os.path.join(os.sep, value)

    # 合作伙伴属性
    @property
    def partners(self) -> List['TPConfigBean']:
        """
        获取合作伙伴配置列表。
        
        Returns:
            List[TPConfigBean]: 合作伙伴配置列表。
        """
        return self._partners

    @partners.setter
    def partners(self, value: List['TPConfigBean']) -> None:
        """
        设置合作伙伴配置列表。
        
        Args:
            value (List[TPConfigBean]): 合作伙伴配置列表。
        """
        self._partners = value if value is not None else []

    def add_partner(self, partner: 'TPConfigBean') -> None:
        """
        添加合作伙伴配置。
        
        Args:
            partner (TPConfigBean): 合作伙伴配置。
        """
        self._partners.append(partner)

    # MQ 配置属性
    @property
    def mqs(self) -> List['MqConfigBean']:
        """
        获取 MQ 配置列表。
        
        Returns:
            List[MqConfigBean]: MQ 配置列表。
        """
        return self._mqs

    @mqs.setter
    def mqs(self, value: List['MqConfigBean']) -> None:
        """
        设置 MQ 配置列表。
        
        Args:
            value (List[MqConfigBean]): MQ 配置列表。
        """
        self._mqs = value if value is not None else []

    def add_mq(self, mq: 'MqConfigBean') -> None:
        """
        添加 MQ 配置。
        
        Args:
            mq (MqConfigBean): MQ 配置。
        """
        self._mqs.append(mq)

    # 控制器属性
    @property
    def controllers(self) -> List['ControllerConfigBean']:
        """
        获取控制器配置列表。
        
        Returns:
            List[ControllerConfigBean]: 控制器配置列表。
        """
        return self._controllers

    @controllers.setter
    def controllers(self, value: List['ControllerConfigBean']) -> None:
        """
        设置控制器配置列表。
        
        Args:
            value (List[ControllerConfigBean]): 控制器配置列表。
        """
        self._controllers = value if value is not None else []

    def add_controller(self, controller: 'ControllerConfigBean') -> None:
        """
        添加控制器配置。
        
        Args:
            controller (ControllerConfigBean): 控制器配置。
        """
        self._controllers.append(controller)

    def __str__(self) -> str:
        """
        返回对象的字符串表示。
        
        Returns:
            str: 对象的字符串表示。
        """
        buffer = [
            "---- trading partners ----\n",
            super().__str__(),
            f"work dir->{self.work_dir}\n",
            f"log dir->{self.log_dir}\n",
            f"backup dir->{self.backup_dir}\n",
            f"tmp dir->{self.tmp_dir}\n"
        ]

        for i, partner in enumerate(self.partners):
            buffer.append(f"---- partner {i} ----\n")
            buffer.append(str(partner))

        for j, controller in enumerate(self.controllers):
            buffer.append(f"---- controller {j} ----\n")
            buffer.append(str(controller))

        for i, mq in enumerate(self.mqs):
            buffer.append(f"---- mq {i} ----\n")
            buffer.append(str(mq))

        return ''.join(buffer)
    