# controller_config_bean.py

from typing import Optional
from .common_thread_bean import CommonThreadBean


class ControllerConfigBean(CommonThreadBean):
    """
    控制器参数的配置bean。
    
    属性:
        is_all_tp (bool): 指定此控制器是否对所有贸易伙伴有效
        process_type (str): 指定相关贸易伙伴的处理类型。
                           有三种处理类型：ALL/IN/OUT
                           - ALL: 处理入站和出站
                           - IN: 仅处理入站文件
                           - OUT: 仅处理出站文件
    """
    
    def __init__(self):
        """
        使用默认值初始化ControllerConfigBean。
        """
        super().__init__()
        self._is_all_tp: bool = False
        self._process_type: Optional[str] = None

    @property
    def is_all_tp(self) -> bool:
        """
        获取此控制器是否对所有贸易伙伴有效。
        
        返回:
            bool: 所有贸易伙伴标志。
        """
        return self._is_all_tp

    @is_all_tp.setter
    def is_all_tp(self, value: bool) -> None:
        """
        设置此控制器是否对所有贸易伙伴有效。
        
        参数:
            value (bool): 所有贸易伙伴标志。
        """
        self._is_all_tp = value

    @property
    def process_type(self) -> Optional[str]:
        """
        获取处理类型。
        
        返回:
            str: 处理类型。
        """
        return self._process_type

    @process_type.setter
    def process_type(self, value: Optional[str]) -> None:
        """
        设置相关贸易伙伴的处理类型。
        
        基本来说，有三种处理类型：
        ALL/IN/OUT
          ALL 表示我们需要处理入站和出站
          IN 表示我们只需要处理入站文件
          OUT 表示我们只需要处理出站文件
        
        参数:
            value (str): 处理类型。
        """
        self._process_type = value

    def __str__(self) -> str:
        """
        将此对象转换为字符串。
        
        返回:
            str: 对象的字符串表示。
        """
        lines = [
            "----------- controller config ------------",
            super().__str__(),
            f"is_all_tp : {self._is_all_tp}",
            f"process_type : {self._process_type}"
        ]
        
        return "\n".join(lines)

# Example usage
if __name__ == "__main__":
    # Example instantiation and usage
    controller_config = ControllerConfigBean() 
    print(controller_config)
 