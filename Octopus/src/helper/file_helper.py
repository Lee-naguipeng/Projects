# -*- coding: utf-8 -*-
"""
FileHelper - 文件操作辅助类
Copyrigth 2005-2010 ISSC Ltd.
创建于 2005-9-7

提供文件追加、复制、权限设置、行数统计等功能
"""

import os
import shutil
import subprocess
import platform
import logging
from pathlib import Path
from typing import Optional, Union, Tuple, BinaryIO
from contextlib import contextmanager
from .common_helper import CommonHelper

class FileHelper(CommonHelper):
    """文件操作辅助类，提供跨平台的文件操作功能"""
    
    # 使用父类的缓冲区大小
    BUFFER_SIZE = CommonHelper.BUFFER_SIZE
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        初始化FileHelper
        
        Args:
            logger: 日志器实例，如果为None则使用默认日志器
        """
        super().__init__(logger_name="FileHelper")
        if logger:
            self.logger = logger
    
    def append_file(
        self, 
        source_file: Union[str, Path], 
        dest_file: Union[str, Path], 
        delete_source: bool = False
    ) -> None:
        """
        将源文件内容追加到目标文件末尾
        
        Args:
            source_file: 源文件路径
            dest_file: 目标文件路径
            delete_source: 是否在追加后删除源文件
            
        Raises:
            FileNotFoundError: 源文件不存在
            PermissionError: 没有文件访问权限
            OSError: 其他文件系统错误
        """
        source_path = Path(source_file)
        dest_path = Path(dest_file)
        
        # 验证源文件是否存在
        if not source_path.exists():
            raise FileNotFoundError(f"Source file does not exist: {source_path}")
        
        self.logger.info(f"Start appending file: {source_path} -> {dest_path}")
        
        # 使用二进制模式读写，确保兼容各种文件类型
        try:
            # 打开目标文件（追加模式）
            with open(dest_path, 'ab') as dest_fd:
                # 打开源文件
                with open(source_path, 'rb') as source_fd:
                    # 分块读取和写入，避免内存溢出
                    while chunk := source_fd.read(self.BUFFER_SIZE):
                        dest_fd.write(chunk)
            
            self.logger.info(f"File append completed: {source_path} -> {dest_path}")
            
            # 如果设置了删除源文件
            if delete_source:
                source_path.unlink()
                self.logger.info(f"Source file deleted: {source_path}")
                
        except Exception as e:
            self.logger.error(f"File append failed: {e}")
            raise
    
    def copy_file_to_directory(
        self, 
        source_file: Union[str, Path], 
        dest_dir: Union[str, Path]
    ) -> None:
        """
        复制文件到指定目录
        
        Args:
            source_file: 源文件路径
            dest_dir: 目标目录路径
            
        Raises:
            FileNotFoundError: 源文件或目标目录不存在
            IsADirectoryError: 源文件是目录
            PermissionError: 没有文件访问权限
        """
        source_path = Path(source_file)
        dest_dir_path = Path(dest_dir)
        
        # 验证源文件
        if not source_path.exists():
            raise FileNotFoundError(f"Source file does not exist: {source_path}")
        if not source_path.is_file():
            raise IsADirectoryError(f"Source path is a directory, not a file: {source_path}")
        
        # 验证目标目录，如果不存在则创建
        if not dest_dir_path.exists():
            dest_dir_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created target directory: {dest_dir_path}")
        
        self.logger.info(f"Start copying file: {source_path} -> {dest_dir_path}")
        
        try:
            # 使用shutil.copy2保持元数据（创建时间、修改时间等）
            shutil.copy2(source_path, dest_dir_path)
            self.logger.info(f"File copy completed: {source_path} -> {dest_dir_path}")
            
        except Exception as e:
            self.logger.error(f"File copy failed: {e}")
            raise
    
    def set_file_permission(self, file_path: Union[str, Path]) -> None:
        """
        设置文件权限（仅在Unix/Linux/AIX系统有效）
        
        Args:
            file_path: 文件路径
            
        Raises:
            FileNotFoundError: 文件不存在
            PermissionError: 没有权限修改文件
        """
        file_path = Path(file_path)
        
        # 验证文件是否存在
        if not file_path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        
        current_os = platform.system()
        
        # Unix/Linux/AIX系统
        if current_os in ("Linux", "AIX", "Darwin"):
            # 注意：MacOS返回Darwin
            
            # 构建chmod命令
            cmd = ["chmod", "770", str(file_path)]
            
            self.logger.info(f"Setting file permissions: {file_path}")
            
            try:
                # 执行命令
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=False  # 不自动抛出异常，我们需要检查返回值
                )
                
                if result.returncode != 0:
                    # 命令执行失败
                    error_msg = result.stderr.strip()
                    self.logger.error(
                        f"Failed to set file permissions: {file_path}\n"
                        f"Error message: {error_msg}"
                    )
                    
                    # 根据错误类型抛出适当的异常
                    if "Permission denied" in error_msg:
                        raise PermissionError(f"Insufficient permissions: {error_msg}")
                    else:
                        raise OSError(f"Failed to set permissions: {error_msg}")
                else:
                    self.logger.info(f"Successfully set file permissions: {file_path}")
                    
            except FileNotFoundError:
                # chmod命令不存在（理论上不应该在Unix系统发生）
                self.logger.error("chmod command not found")
                raise
            except Exception as e:
                self.logger.error(f"Exception occurred while setting file permissions: {e}")
                raise
        
        # Windows系统
        elif current_os == "Windows":
            self.logger.info(
                f"Windows system does not require Unix permissions: {file_path}\n"
                f"Please use Windows File Explorer or icacls command to set permissions"
            )
            # Windows没有chmod，但我们可以尝试设置基本的文件属性
            try:
                # 移除只读属性
                os.chmod(file_path, 0o666)  # os.chmod on Windows has limitations
                self.logger.info(f"Basic file permissions set: {file_path}")
            except Exception as e:
                self.logger.warning(f"Failed to set Windows file permissions: {e}")
        
        # 其他操作系统
        else:
            self.logger.warning(
                f"Unsupported operating system '{current_os}', skipping permission setting: {file_path}"
            )
    
    def count_lines(self, file_path: Union[str, Path]) -> int:
        """
        统计文件行数
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件行数
            
        Raises:
            FileNotFoundError: 文件不存在
            UnicodeDecodeError: 文件编码问题
        """
        file_path = Path(file_path)
        
        # 验证文件
        if not file_path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        if not file_path.is_file():
            raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")
        
        self.logger.info(f"Counting lines: {file_path}")
        
        line_count = 0
        
        try:
            # 尝试自动检测编码并读取文件
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                for line_count, _ in enumerate(f, 1):
                    pass  # 只需要计数，不需要内容
                    
        except UnicodeDecodeError:
            # 如果UTF-8失败，尝试其他编码
            self.logger.info(f"UTF-8 decoding failed, trying other encodings: {file_path}")
            
            # 尝试常见编码
            encodings = ['gbk', 'gb2312', 'latin-1', 'iso-8859-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                        for line_count, _ in enumerate(f, 1):
                            pass
                    break  # 成功读取，跳出循环
                except UnicodeDecodeError:
                    continue
            else:
                # 所有编码都失败，尝试二进制模式（只统计换行符）
                self.logger.warning(f"Cannot decode file with any encoding, using binary mode: {file_path}")
                with open(file_path, 'rb') as f:
                    line_count = sum(1 for _ in f)
        
        self.logger.info(f"Line count completed: {file_path} -> {line_count} lines")
        return line_count
    
    # Pythonic的附加功能
    
    def read_file_chunks(
        self, 
        file_path: Union[str, Path], 
        chunk_size: int = None
    ) -> bytes: # type: ignore
        """
        以生成器方式读取文件块（内存高效）
        
        Args:
            file_path: 文件路径
            chunk_size: 块大小，默认为BUFFER_SIZE
            
        Yields:
            文件数据块
        """
        if chunk_size is None:
            chunk_size = self.BUFFER_SIZE
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                yield chunk
    
    @contextmanager
    def safe_open(self, file_path: Union[str, Path], mode: str = 'r', encoding: str = 'utf-8'):
        """
        安全打开文件的上下文管理器
        
        Args:
            file_path: 文件路径
            mode: 打开模式
            encoding: 文件编码，默认为utf-8
            
        Yields:
            文件对象
            
        Example:
            with helper.safe_open('test.txt') as f:
                content = f.read()
        """
        file_path = Path(file_path)
        f = None
        
        try:
            if 'b' in mode:
                f = open(file_path, mode)
            else:
                f = open(file_path, mode, encoding=encoding)
            yield f
        except Exception as e:
            self.logger.error(f"Failed to open file: {file_path} - {e}")
            raise
        finally:
            if f:
                f.close()
    
    def find_files(
        self, 
        directory: Union[str, Path], 
        pattern: str = "*",
        recursive: bool = False
    ) -> list:
        """
        查找匹配模式的文件
        
        Args:
            directory: 目录路径
            pattern: 文件模式，如 "*.txt"
            recursive: 是否递归搜索子目录
            
        Returns:
            匹配的文件路径列表
        """
        dir_path = Path(directory)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory does not exist: {dir_path}")
        
        if recursive:
            return list(dir_path.rglob(pattern))
        else:
            return list(dir_path.glob(pattern))
    
    def get_file_info(self, file_path: Union[str, Path]) -> dict:
        """
        获取文件详细信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            包含文件信息的字典
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {path}")
        
        stats = path.stat()
        
        return {
            "path": str(path.absolute()),
            "name": path.name,
            "size": stats.st_size,
            "created": stats.st_ctime,
            "modified": stats.st_mtime,
            "accessed": stats.st_atime,
            "is_file": path.is_file(),
            "is_dir": path.is_dir(),
            "parent": str(path.parent),
        }
    
    def create_backup(
        self, 
        file_path: Union[str, Path], 
        backup_suffix: str = ".bak"
    ) -> Path:
        """
        创建文件备份
        
        Args:
            file_path: 原文件路径
            backup_suffix: 备份文件后缀
            
        Returns:
            备份文件路径
        """
        import datetime
        
        source = Path(file_path)
        
        if not source.exists():
            raise FileNotFoundError(f"Source file does not exist: {source}")
        
        backup_path = source.with_suffix(source.suffix + backup_suffix)
        
        # 如果备份文件已存在，添加时间戳
        if backup_path.exists():
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = source.with_suffix(f"{source.suffix}.{timestamp}{backup_suffix}")
        
        shutil.copy2(source, backup_path)
        self.logger.info(f"Created backup file: {source} -> {backup_path}")
        
        return backup_path


# 模块级别的便捷函数
def get_file_helper() -> FileHelper:
    """获取共享的FileHelper实例"""
    if not hasattr(get_file_helper, "_shared_instance"):
        get_file_helper._shared_instance = FileHelper()
    return get_file_helper._shared_instance


def main() -> None:
    """主函数 - 示例和测试"""
    import tempfile
    
    helper = FileHelper()
    
    print("=== FileHelper Function Demonstration ===")
    
    # 创建测试文件
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        
        # 测试文件追加
        print("\n1. Testing file append function:")
        file1 = temp_dir / "file1.txt"
        file2 = temp_dir / "file2.txt"
        
        # 修复：在Windows上使用UTF-8编码写入文件
        try:
            file1.write_text("This is content of file1\n", encoding='utf-8')
            file2.write_text("This is content of file2\n", encoding='utf-8')
        except UnicodeEncodeError:
            # 如果默认编码失败，尝试使用二进制模式
            file1.write_bytes(b"This is content of file1\n")
            file2.write_bytes(b"This is content of file2\n")
        
        helper.append_file(file2, file1)
        
        # 使用正确的编码读取文件
        try:
            print(f"Content after append:\n{file1.read_text(encoding='utf-8')}")
        except UnicodeDecodeError:
            print(f"Binary content after append:\n{file1.read_bytes()[:100]}...")
        
        # 测试复制文件到目录
        print("\n2. Testing file copy function:")
        dest_dir = temp_dir / "dest_dir"
        helper.copy_file_to_directory(file1, dest_dir)
        print(f"File copied to: {dest_dir}")
        
        # 测试统计行数
        print("\n3. Testing line count function:")
        line_count = helper.count_lines(file1)
        print(f"Number of lines: {line_count}")
        
        # 测试文件权限设置（仅在Unix系统有效）
        print("\n4. Testing file permission setting:")
        try:
            helper.set_file_permission(file1)
        except Exception as e:
            print(f"Permission setting notes: {e}")
        
        # 测试Pythonic功能
        print("\n5. Testing Pythonic features:")
        
        # 使用生成器读取文件块
        print("Reading file with generator:")
        for i, chunk in enumerate(helper.read_file_chunks(file1, chunk_size=10)):
            print(f"Chunk {i+1}: {chunk[:20]}...")
        
        # 使用上下文管理器
        print("\nUsing safe context manager:")
        with helper.safe_open(file1) as f:
            content = f.read()
            print(f"File content: {content[:50]}...")
        
        # 查找文件
        print("\nFinding test files:")
        files = helper.find_files(temp_dir, "*.txt")
        for f in files:
            print(f"Found file: {f}")
        
        # 获取文件信息
        print("\nGetting file information:")
        info = helper.get_file_info(file1)
        for key, value in info.items():
            print(f"{key}: {value}")
    
    print("\n=== Demo Completed ===")


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 运行演示
    main()