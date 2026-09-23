from typing import Optional
from .ftp_config_bean import FtpConfigBean
from .mq_config_bean import MqConfigBean
from .in_out_config_bean import InOutConfigBean

class OutConfigBean(InOutConfigBean):
    """
    出站参数配置 Bean。
    
    这个类用于配置出站(outbound)相关的参数，继承自 InOutConfigBean 基类。
    主要包含目录配置以及 FTP 和 MQ 的配置信息。
    """

    def __init__(self):
        """
        初始化 OutConfigBean 实例。
        """
        super().__init__()

    def __str__(self) -> str:
        """
        将对象转换为字符串表示形式。
        
        Returns:
            str: 对象的字符串表示。
        """
        lines = []
        
        # 添加目录信息
        lines.append(f"dir : {self.dir}\n")
        
        # 如果 FTP 配置存在，则添加到输出中
        if self.ftp is not None:
            lines.append(str(self.ftp))
            
        # 如果 MQ 配置存在，则添加到输出中
        if self.mq is not None:
            lines.append(str(self.mq))
            
        return ''.join(lines)

    @staticmethod
    def main() -> None:
        """
        测试方法。
        """
        pass
