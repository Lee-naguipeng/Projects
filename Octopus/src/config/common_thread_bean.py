# common_thread_bean.py

from typing import Optional
from pathlib import Path
from .send_msg_config_bean import SendMsgConfigBean
from .private_config import PrivateConfig

class CommonThreadBean:
    """
    所有线程的通用配置。
    
    每个将作为线程运行的类，包括Stub.class、
    Controller.class、CommonTP.class及其所有子类都可以配置这些属性。
    """
    
    def __init__(self):
        """使用默认值初始化CommonThreadBean。"""
        self._is_send_error: bool = False
        self._error_msg: Optional['SendMsgConfigBean'] = None
        self._is_send_alive: bool = False
        self._alive_msg: Optional['SendMsgConfigBean'] = None
        self._app_trace_flag: bool = False
        self._mq_trace_flag: bool = False
        self._name: Optional[str] = None
        self._run_type: Optional[str] = None
        self._log_retention: int = 0
        self._log_dir: Optional[str] = None
        self._run_flag: bool = False
        self._log_level: int = 1
        self._sleep_time: int = 30
        self._private_config_file_name: Optional[str] = None
        self._private_config: Optional['PrivateConfig'] = None

    def copy(self) -> 'CommonThreadBean':
        """
        创建此配置bean的副本。
        
        返回:
            CommonThreadBean: 具有相同属性的新实例。
        """
        new_config = CommonThreadBean()
        new_config._is_send_error = self._is_send_error
        new_config._error_msg = self._error_msg
        new_config._is_send_alive = self._is_send_alive
        new_config._alive_msg = self._alive_msg
        new_config._app_trace_flag = self._app_trace_flag
        new_config._mq_trace_flag = self._mq_trace_flag
        new_config._name = self._name
        new_config._run_type = self._run_type
        new_config._log_retention = self._log_retention
        new_config._log_dir = self._log_dir
        new_config._run_flag = self._run_flag
        new_config._log_level = self._log_level
        new_config._sleep_time = self._sleep_time
        new_config._private_config_file_name = self._private_config_file_name
        new_config._private_config = self._private_config
        return new_config

    # --- 属性方法 ---

    @property
    def is_send_error(self) -> bool:
        """
        获取是否发送错误消息。
        
        返回:
            bool: 是否发送错误消息。
        """
        return self._is_send_error

    @is_send_error.setter
    def is_send_error(self, value: bool) -> None:
        """
        设置是否发送错误消息。
        
        参数:
            value (bool): 是否发送错误消息。
        """
        self._is_send_error = value

    @property
    def error_msg(self) -> Optional['SendMsgConfigBean']:
        """
        获取错误消息配置。
        
        返回:
            SendMsgConfigBean: 错误消息配置。
        """
        return self._error_msg

    @error_msg.setter
    def error_msg(self, value: Optional['SendMsgConfigBean']) -> None:
        """
        设置错误消息配置。
        
        参数:
            value (SendMsgConfigBean): 错误消息配置。
        """
        self._error_msg = value

    @property
    def is_send_alive(self) -> bool:
        """
        获取是否发送活动消息。
        
        返回:
            bool: 是否发送活动消息。
        """
        return self._is_send_alive

    @is_send_alive.setter
    def is_send_alive(self, value: bool) -> None:
        """
        设置是否发送活动消息。
        
        参数:
            value (bool): 是否发送活动消息。
        """
        self._is_send_alive = value

    @property
    def alive_msg(self) -> Optional['SendMsgConfigBean']:
        """
        获取正常消息配置。
        
        返回:
            SendMsgConfigBean: 正常消息配置。
        """
        return self._alive_msg

    @alive_msg.setter
    def alive_msg(self, value: Optional['SendMsgConfigBean']) -> None:
        """
        设置正常消息配置。
        
        参数:
            value (SendMsgConfigBean): 正常消息配置。
        """
        self._alive_msg = value

    @property
    def app_trace_flag(self) -> bool:
        """
        获取应用程序跟踪标志。
        
        返回:
            bool: 应用程序跟踪标志。
        """
        return self._app_trace_flag

    @app_trace_flag.setter
    def app_trace_flag(self, value: bool) -> None:
        """
        设置应用程序跟踪标志。
        
        参数:
            value (bool): 应用程序跟踪标志。
        """
        self._app_trace_flag = value

    @property
    def mq_trace_flag(self) -> bool:
        """
        获取是否跟踪MQ。
        
        返回:
            bool: 是否跟踪MQ。
        """
        return self._mq_trace_flag

    @mq_trace_flag.setter
    def mq_trace_flag(self, value: bool) -> None:
        """
        设置是否跟踪MQ。
        
        参数:
            value (bool): 是否跟踪MQ。
        """
        self._mq_trace_flag = value

    @property
    def name(self) -> Optional[str]:
        """
        获取线程名称。
        
        返回:
            str: 线程名称。
        """
        return self._name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        """
        设置线程名称。
        
        参数:
            value (str): 线程名称。
        """
        self._name = value

    @property
    def run_type(self) -> Optional[str]:
        """
        获取运行环境类型。
        
        返回:
            str: 运行环境类型。
        """
        return self._run_type

    @run_type.setter
    def run_type(self, value: Optional[str]) -> None:
        """
        设置运行环境类型。
        
        参数:
            value (str): 运行环境类型。
        """
        self._run_type = value

    @property
    def log_retention(self) -> int:
        """
        获取日志文件保留数量。
        
        返回:
            int: 日志文件保留数量。
        """
        return self._log_retention

    @log_retention.setter
    def log_retention(self, value: int) -> None:
        """
        设置日志文件保留数量。
        
        参数:
            value (int): 日志文件保留数量。
        """
        self._log_retention = value

    @property
    def log_dir(self) -> Optional[str]:
        """
        获取日志文件路径。
        
        返回:
            str: 日志文件路径。
        """
        return self._log_dir

    @log_dir.setter
    def log_dir(self, value: Optional[str]) -> None:
        """
        设置日志文件路径。
        
        参数:
            value (str): 日志文件路径。
        """
        self._log_dir = value

    @property
    def run_flag(self) -> bool:
        """
        获取线程是否应该运行。
        
        返回:
            bool: 线程是否应该运行。
        """
        return self._run_flag

    @run_flag.setter
    def run_flag(self, value: bool) -> None:
        """
        设置线程是否应该运行。
        
        参数:
            value (bool): 线程是否应该运行。
        """
        self._run_flag = value

    @property
    def log_level(self) -> int:
        """
        获取日志消息级别。
        
        日志级别:
        4 -> 无日志消息，程序不输出任何消息
        3 -> 仅错误消息，包括异常消息
        2 -> 错误消息和警告消息
        1 -> 错误消息、警告消息和普通程序输出
        0 -> 详细消息，包括所有内容
        
        返回:
            int: 日志消息级别。
        """
        return self._log_level

    @log_level.setter
    def log_level(self, value: int) -> None:
        """
        设置日志消息级别。
        
        参数:
            value (int): 日志消息级别。
        """
        self._log_level = value

    @property
    def sleep_time(self) -> int:
        """
        获取线程应休眠的持续时间（以秒为单位）。
        
        返回:
            int: 休眠时间（秒）。
        """
        return self._sleep_time

    @sleep_time.setter
    def sleep_time(self, value: int) -> None:
        """
        设置线程应休眠的持续时间（以秒为单位）。
        
        参数:
            value (int): 休眠时间（秒）。
        """
        self._sleep_time = value

    @property
    def private_config_file_name(self) -> Optional[str]:
        """
        获取私有配置文件名。
        
        返回:
            str: 私有配置文件名。
        """
        return self._private_config_file_name

    @private_config_file_name.setter
    def private_config_file_name(self, value: Optional[str]) -> None:
        """
        设置私有配置文件名。
        
        参数:
            value (str): 私有配置文件名。
        """
        self._private_config_file_name = value

    @property
    def private_config(self) -> Optional['PrivateConfig']:
        """
        获取私有配置。
        
        返回:
            PrivateConfig: 私有配置。
        """
        return self._private_config

    @private_config.setter
    def private_config(self, value: Optional['PrivateConfig']) -> None:
        """
        设置私有配置。
        
        参数:
            value (PrivateConfig): 私有配置。
        """
        self._private_config = value

    def __str__(self) -> str:
        """
        返回通用线程配置的字符串表示。
        
        返回:
            str: 字符串表示。
        """
        lines = [
            "------------- common thread bean config -------------",
            f"name->{self._name}",
            f"privateConfigFileName->{self._private_config_file_name}"
        ]
        
        if self._private_config is not None:
            lines.append(f"private config->\n{self._private_config}")
        else:
            lines.append("private config->null")
            
        lines.append(f"isSendError->{self._is_send_error}")
        
        if self._error_msg is not None:
            lines.append(f"errorMsg->\n{self._error_msg}")
        else:
            lines.append("errorMsg->null")
            
        lines.append(f"isSendAlive->{self._is_send_alive}")
        
        if self._alive_msg is not None:
            lines.append(f"aliveMsg->\n{self._alive_msg}")
        else:
            lines.append("aliveMsg->null")
            
        lines.extend([
            f"appTraceFlag->{self._app_trace_flag}",
            f"mqTraceFlag->{self._mq_trace_flag}",
            f"runType->{self._run_type}",
            f"logRetention->{self._log_retention}",
            f"logDir->{self._log_dir}",
            f"runFlag->{self._run_flag}",
            f"logLevel->{self._log_level}",
            f"sleepTime->{self._sleep_time}"
        ])
        
        return "\n".join(lines)

if __name__ == "__main__":
    # Test code
  Common_config = CommonThreadBean()
  Common_config.private_config = PrivateConfig(Path("tpdConfig.xml"))
  Common_config.private_config.parse()
  print (Common_config)
