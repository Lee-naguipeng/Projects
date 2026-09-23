# file_config_bean.py

from typing import Optional, TYPE_CHECKING
from .common_config_bean import CommonConfigBean

if TYPE_CHECKING:
    pass

class FileConfigBean(CommonConfigBean):
    """
    Configure bean of file parameters.
    """
    
    def __init__(self):
        """Initialize the FileConfigBean with default values."""
        # From CommonConfigBean
        super().__init__()
        
        # FileConfigBean specific attributes
        self._dir: Optional[str] = None
        self._tmp_dir: Optional[str] = None
        self._archive_dir: Optional[str] = None
        self._prefix_file_name: Optional[str] = None
        self._suffix_file_name: Optional[str] = None
        self._if_add_random_number: str = "N"

    def copy(self) -> 'FileConfigBean':
        """
        Create a copy of this configuration bean.
        
        Returns:
            FileConfigBean: A new instance with the same properties.
        """
        # Get parent copy
        parent_copy = super().copy()
        
        # Create new instance
        bean = FileConfigBean()
        
        # Copy parent attributes
        bean._name = parent_copy._name
        bean._id = parent_copy._id
        bean._extend = parent_copy._extend
        bean._mqs = parent_copy._mqs.copy()
        bean._ftps = parent_copy._ftps.copy()
        bean._emails = parent_copy._emails.copy()
        bean._files = parent_copy._files.copy()
        
        # Copy FileConfigBean specific properties
        bean._dir = self._dir
        bean._tmp_dir = self._tmp_dir
        bean._archive_dir = self._archive_dir
        bean._prefix_file_name = self._prefix_file_name
        bean._suffix_file_name = self._suffix_file_name
        bean._if_add_random_number = self._if_add_random_number
        
        return bean

    # --- 属性方法 ---

    @property
    def dir(self) -> Optional[str]:
        """
        获取目录路径。
        
        返回:
            str: 目录路径。
        """
        return self._dir

    @dir.setter
    def dir(self, value: Optional[str]) -> None:
        """
        设置目录路径。
        
        参数:
            value (str): 目录路径。
        """
        self._dir = value

    @property
    def tmp_dir(self) -> Optional[str]:
        """
        获取临时目录路径。
        
        返回:
            str: 临时目录路径。
        """
        return self._tmp_dir

    @tmp_dir.setter
    def tmp_dir(self, value: Optional[str]) -> None:
        """
        设置临时目录路径。
        
        参数:
            value (str): 临时目录路径。
        """
        self._tmp_dir = value

    @property
    def archive_dir(self) -> Optional[str]:
        """
        获取归档目录路径。
        
        返回:
            str: 归档目录路径。
        """
        return self._archive_dir

    @archive_dir.setter
    def archive_dir(self, value: Optional[str]) -> None:
        """
        设置归档目录路径。
        
        参数:
            value (str): 归档目录路径。
        """
        self._archive_dir = value

    @property
    def prefix_file_name(self) -> Optional[str]:
        """
        获取文件名前缀。
        
        返回:
            str: 文件名前缀。
        """
        return self._prefix_file_name

    @prefix_file_name.setter
    def prefix_file_name(self, value: Optional[str]) -> None:
        """
        设置文件名前缀。
        
        参数:
            value (str): 文件名前缀。
        """
        self._prefix_file_name = value

    @property
    def suffix_file_name(self) -> Optional[str]:
        """
        获取文件名后缀。
        
        返回:
            str: 文件名后缀。
        """
        return self._suffix_file_name

    @suffix_file_name.setter
    def suffix_file_name(self, value: Optional[str]) -> None:
        """
        设置文件名后缀。
        
        参数:
            value (str): 文件名后缀。
        """
        self._suffix_file_name = value

    @property
    def if_add_random_number(self) -> str:
        """
        获取是否添加随机数标志。
        
        返回:
            str: 是否添加随机数标志 ('Y' 或 'N')。
        """
        return self._if_add_random_number

    @if_add_random_number.setter
    def if_add_random_number(self, value: str) -> None:
        """
        设置是否添加随机数标志。
        
        参数:
            value (str): 是否添加随机数标志 ('Y' 或 'N')。
        """
        self._if_add_random_number = value

    def __str__(self) -> str:
        """
        返回文件配置的字符串表示。
        
        返回:
            str: 字符串表示。
        """
        lines = [
            "--------- file config -----------",
            super().__str__(),
            f"dir : {self._dir}",
            f"archive_dir : {self._archive_dir}",
            f"prefix_file_name : {self._prefix_file_name}",
            f"if_add_random_number : {self._if_add_random_number}"
        ]
        return "\n".join(lines) + "\n"
          
    def __repr__(self) -> str:
        """Detailed representation for debugging."""
        return (f"FileConfigBean(dir={self._dir!r}, "
                f"archive_dir={self._archive_dir!r}, "
                f"prefix_file_name={self._prefix_file_name!r}, "
                f"if_add_random_number={self._if_add_random_number!r})")


if __name__ == "__main__":
    # Test code can be added here
    config=FileConfigBean() 
    config_copy = config.copy()
    config_copy.name="test_config2"
    print(repr(config_copy.name))
    print(repr(config_copy))
