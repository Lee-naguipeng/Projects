import os
from typing import List

class ByteArrayHelper:
    """更Pythonic的字节操作工具类"""
    
    @staticmethod
    def hex_format(data: bytes, 
                  bytes_per_line: int = 30, 
                  group_size: int = 15, 
                  separator: str = " ") -> str:
        """
        将字节数组格式化为十六进制字符串
        
        Args:
            data: 字节数组
            bytes_per_line: 每行字节数
            group_size: 每组字节数
            separator: 字节分隔符
            
        Returns:
            格式化的十六进制字符串
        """
        if not data:
            return ""
        
        # 使用生成器表达式和列表推导式，更Pythonic
        lines = []
        for i in range(0, len(data), bytes_per_line):
            line_bytes = data[i:i + bytes_per_line]
            
            # 每组字节
            groups = []
            for j in range(0, len(line_bytes), group_size):
                group = line_bytes[j:j + group_size]
                hex_group = separator.join(f"{b:02x}" for b in group)
                groups.append(hex_group)
            
            # 用制表符连接各组
            lines.append("\t".join(groups))
        
        return "\n".join(lines)
    
    @staticmethod
    def filter_bytes(data: bytes, predicate) -> bytes:
        """
        使用谓词函数过滤字节
        
        Args:
            data: 原始字节数组
            predicate: 谓词函数，接受一个字节返回布尔值
            
        Returns:
            过滤后的字节数组
        """
        return bytes(b for b in data if predicate(b))
    
    @staticmethod
    def map_bytes(data: bytes, transform) -> bytes:
        """
        对每个字节应用变换函数
        
        Args:
            data: 原始字节数组
            transform: 变换函数，接受一个字节返回一个字节
            
        Returns:
            变换后的字节数组
        """
        return bytes(transform(b) for b in data)
    
    @staticmethod
    def strip_trailing(data: bytes, byte_to_strip: int) -> bytes:
        """
        移除末尾指定的字节（类似字符串的rstrip）
        
        Args:
            data: 原始字节数组
            byte_to_strip: 要移除的字节
            
        Returns:
            移除末尾指定字节后的字节数组
        """
        # 使用bytes的rstrip方法（需要转换为字节串）
        return data.rstrip(bytes([byte_to_strip]))
    
    @staticmethod
    def chunk_bytes(data: bytes, chunk_size: int) -> List[bytes]:
        """
        将字节数组分块
        
        Args:
            data: 原始字节数组
            chunk_size: 块大小
            
        Returns:
            分块后的字节数组列表
        """
        return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


if __name__ == "__main__":

    
    # 测试更Pythonic的版本
    helper = ByteArrayHelper()
    test_bytes = b"Python is awesome!" * 5
    
    print("更Pythonic的hex_format输出:")
    print(helper.hex_format(test_bytes, bytes_per_line=20, group_size=5))
    print()
    
    print("过滤ASCII可打印字符:")
    printable_bytes = helper.filter_bytes(test_bytes, lambda b: 32 <= b <= 126)
    print(f"结果: {printable_bytes}")
    print()
    
    print("将小写字母转换为大写:")
    uppercase_bytes = helper.map_bytes(test_bytes, lambda b: b - 32 if 97 <= b <= 122 else b)
    print(f"结果: {uppercase_bytes}")
    print()
    
    print("移除末尾的空格:")
    data_with_spaces = b"Hello World   "
    stripped = helper.strip_trailing(data_with_spaces, ord(' '))
    print(f"原始: {data_with_spaces}")
    print(f"移除空格后: {stripped}")
    print()
    
    print("分块显示:")
    chunks = helper.chunk_bytes(b"0123456789ABCDEF", 4)
    for i, chunk in enumerate(chunks):
        print(f"块{i+1}: {chunk.hex()}")