# private_filter_config_bean.py
"""
采用Pythonic接口的私有过滤器配置bean。
"""

class PrivateFilterConfigBean:
    """
    私有过滤器参数的配置bean。
    """
    
    def __init__(self):
        """
        使用默认值初始化PrivateFilterConfigBean。
        """
        self._origin_char: int = -1
        self._replacement_char: int = -1
        self._trim_number: int = -1
        self._fix_length: int = -1

    # 源字符属性
    @property
    def origin_char(self) -> int:
        """
        获取源字符。
        
        返回:
            int: 源字符值。
        """
        return self._origin_char

    @origin_char.setter
    def origin_char(self, value: int) -> None:
        """
        设置源字符。
        
        参数:
            value (int): 源字符值。
        """
        self._origin_char = value

    # 替换字符属性
    @property
    def replacement_char(self) -> int:
        """
        获取替换字符。
        
        返回:
            int: 替换字符值。
        """
        return self._replacement_char

    @replacement_char.setter
    def replacement_char(self, value: int) -> None:
        """
        设置替换字符。
        
        参数:
            value (int): 替换字符值。
        """
        self._replacement_char = value

    # 修剪数量属性
    @property
    def trim_number(self) -> int:
        """
        获取修剪数量。
        
        返回:
            int: 修剪数量值。
        """
        return self._trim_number

    @trim_number.setter
    def trim_number(self, value: int) -> None:
        """
        设置修剪数量。
        
        参数:
            value (int): 修剪数量值。
        """
        self._trim_number = value

    # 固定长度属性
    @property
    def fix_length(self) -> int:
        """
        获取固定长度。
        
        返回:
            int: 固定长度值。
        """
        return self._fix_length

    @fix_length.setter
    def fix_length(self, value: int) -> None:
        """
        设置固定长度。
        
        参数:
            value (int): 固定长度值。
        """
        self._fix_length = value

    def __str__(self) -> str:
        """
        将此对象转换为字符串。
        
        返回:
            str: 对象的字符串表示。
        """
        lines = [
            "-------------- private filter config --------------",
            f"originChar : {self._origin_char}",
            f"replacementChar : {self._replacement_char}",
            f"trimNumber : {self._trim_number}",
            f"fixLength : {self._fix_length}"
        ]
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        """
        用于调试的详细表示。
        
        返回:
            str: 详细的字符串表示。
        """
        return (f"PrivateFilterConfigBean(origin_char={self._origin_char}, "
                f"replacement_char={self._replacement_char}, "
                f"trim_number={self._trim_number}, "
                f"fix_length={self._fix_length})")


# 示例用法和测试
if __name__ == "__main__":
    # 测试私有过滤器配置
    filter_config = PrivateFilterConfigBean()
    
    # 设置过滤器属性
    filter_config.origin_char = 65  # 'A'
    filter_config.replacement_char = 66  # 'B'
    filter_config.trim_number = 10
    filter_config.fix_length = 20
    
    print("私有过滤器配置:")
    print(filter_config)
    print()
    
    print("调试表示:")
    print(repr(filter_config))