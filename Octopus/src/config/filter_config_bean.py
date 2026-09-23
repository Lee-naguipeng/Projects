# filter_config_bean.py
"""
采用Pythonic接口的过滤器配置bean。
"""

from typing import Optional
from .private_filter_config_bean import PrivateFilterConfigBean


class FilterConfigBean:
    """
    过滤器参数的配置bean。
    """
    
    def __init__(self):
        """
        使用默认值初始化FilterConfigBean。
        """
        self._name: Optional[str] = None
        self._filter_class: Optional[str] = None
        self._private_config: Optional[str] = None
        self._private_filter: Optional['PrivateFilterConfigBean'] = None

    # 名称属性
    @property
    def name(self) -> str:
        """
        获取配置段的标识符。
        
        返回:
            str: 名称值，如果未设置则返回空字符串。
        """
        return self._name if self._name is not None else ""

    @name.setter
    def name(self, value: str) -> None:
        """
        设置配置段的标识符。
        
        参数:
            value (str): 名称值。
        """
        self._name = value

    # 过滤器类属性
    @property
    def filter_class(self) -> Optional[str]:
        """
        获取过滤器的类名。
        
        返回:
            str: 过滤器类名。
        """
        return self._filter_class

    @filter_class.setter
    def filter_class(self, value: str) -> None:
        """
        设置过滤器的类名。
        
        参数:
            value (str): 过滤器类名。
        """
        self._filter_class = value

    # 私有配置属性
    @property
    def private_config(self) -> str:
        """
        获取过滤器的私有配置。
        
        返回:
            str: 用XML标签包装的私有配置。
        """
        if self._private_config is not None:
            return f"{self._private_config}</privateConfig>"
        else:
            return "<privateConfig/>"

    @private_config.setter
    def private_config(self, value: str) -> None:
        """
        设置过滤器的私有配置。
        
        参数:
            value (str): 私有配置字符串。
        """
        if value is not None:
            if self._private_config is None:
                self._private_config = f"<privateConfig>{value}"
            else:
                self._private_config += value

    # 私有过滤器属性
    @property
    def private_filter(self) -> 'PrivateFilterConfigBean':
        """
        获取私有过滤器配置。
        
        返回:
            PrivateFilterConfigBean: 私有过滤器配置。
        """
        if self._private_filter is None:
            self._private_filter = PrivateFilterConfigBean()
        return self._private_filter

    @private_filter.setter
    def private_filter(self, value: 'PrivateFilterConfigBean') -> None:
        """
        设置私有过滤器配置。
        
        参数:
            value (PrivateFilterConfigBean): 私有过滤器配置。
        """
        self._private_filter = value

    def __str__(self) -> str:
        """
        将此对象转换为字符串。
        
        返回:
            str: 对象的字符串表示。
        """
        lines = [
            "-------------- filter config --------------",
            f"name : {self.name}",
            f"filter_class : {self.filter_class}",
            f"private_config : {self.private_config}"
        ]
        return "\n".join(lines) + "\n"
    
    # Example usage and testing
if __name__ == "__main__":

    filter_config =FilterConfigBean()
    filter_config.name='lizhiyuan'
    filter_config.private_filter.trim_number = 10
    print(filter_config)

