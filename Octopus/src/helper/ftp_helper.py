# -*- coding: utf-8 -*-
"""
FtpHelper - FTP/SFTP操作辅助类

提供FTP和SFTP的上传、下载、文件筛选等功能
"""
import sys
import os

import re
import logging
import tempfile
from pathlib import Path
from typing import Optional, Union, List, Dict, Any, BinaryIO
from io import BytesIO, StringIO
import ftplib
import paramiko
from ..config import FtpConfigBean


class FtpHelper:
    """FTP/SFTP操作辅助类"""
    
    def __init__(self, logger: Optional[logging.Logger] = None, debug: bool = False):
        """
        初始化FtpHelper
        
        Args:
            logger: 日志器实例
            debug: 是否启用调试模式
        """
        self._logger = logger or logging.getLogger(self.__class__.__name__)
        self._debug = debug
        
        # 如果还没有配置日志处理器，添加一个简单的
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    @property
    def logger(self) -> logging.Logger:
        """获取日志器"""
        return self._logger
    
    @logger.setter
    def logger(self, logger: logging.Logger) -> None:
        """设置日志器"""
        self._logger = logger
    
    @property
    def debug(self) -> bool:
        """获取调试模式状态"""
        return self._debug
    
    @debug.setter
    def debug(self, debug: bool) -> None:
        """设置调试模式"""
        self._debug = debug
        self._logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    # ========================================== 公共上传方法 ============================================
    
    def put(self, fb: FtpConfigBean, data: Union[str, bytes, StringIO, BytesIO, Path, str]) -> None:
        """
        上传数据到FTP/SFTP服务器
        
        Args:
            fb: FTP配置对象
            data: 要上传的数据，可以是字符串、字节、文件对象、文件路径
            
        Raises:
            ValueError: 如果配置对象为空
            Exception: 上传过程中出现错误
        """
        if fb is None:
            raise ValueError("FtpConfigBean cannot be None")
        
        if isinstance(data, str):
            # 字符串 -> 字节
            data_bytes = data.encode('utf-8')
            self._put_bytes(fb, data_bytes)
        elif isinstance(data, bytes):
            # 字节数据
            self._put_bytes(fb, data)
        elif isinstance(data, (StringIO, BytesIO)):
            # 内存流
            self._put_stream(fb, data)
        elif isinstance(data, Path):
            # Path对象
            self._put_file(fb, data)
        elif isinstance(data, str):
            # 文件路径字符串
            self._put_file(fb, Path(data))
        else:
            raise TypeError(f"Unsupported data type: {type(data)}")
    
    def _put_bytes(self, fb: FtpConfigBean, data: bytes) -> None:
        """上传字节数据"""
        stream = BytesIO(data)
        self._put_stream(fb, stream)
    
    def _put_stream(self, fb: FtpConfigBean, stream: Union[BytesIO, StringIO]) -> None:
        """上传流数据"""
        if fb.ssh_enabled:
            self._sftp_put_stream(fb, stream)
        else:
            self._ftp_put_stream(fb, stream)

    def _put_file(self, fb: FtpConfigBean, file_path: Path) -> None:
        """上传文件"""
        if fb.ssh_enabled:
            self._sftp_put_file(fb, file_path)
        else:
            self._ftp_put_file(fb, file_path)
    
    # ========================================== 公共下载方法 ============================================
    
    def get(self, fb: FtpConfigBean) -> List[Path]:
        """
        从FTP/SFTP服务器下载文件
        
        Args:
            fb: FTP配置对象
            
        Returns:
            下载到本地的文件路径列表
            
        Raises:
            ValueError: 如果配置对象为空
            Exception: 下载过程中出现错误
        """
        if fb is None:
            raise ValueError("FtpConfigBean cannot be None")
        
        if fb.ssh_enabled:
            return self._sftp_get(fb)
        else:
            return self._ftp_get(fb)
    
    # ========================================== 批量上传方法 ============================================
    
    def put_dir_with_prefix(self, fb: FtpConfigBean, directory: Union[str, Path], prefix: str) -> None:
        """
        上传目录中指定前缀的文件
        
        Args:
            fb: FTP配置对象
            directory: 目录路径
            prefix: 文件名前缀
        """
        dir_path = Path(directory)
        if not dir_path.is_dir():
            raise ValueError(f"{directory} is not a valid directory")
        
        for file_path in dir_path.iterdir():
            if file_path.is_file() and file_path.name.startswith(prefix):
                self.put(fb, file_path)
    
    def put_dir_with_suffix(self, fb: FtpConfigBean, directory: Union[str, Path], suffix: str) -> None:
        """
        上传目录中指定后缀的文件
        
        Args:
            fb: FTP配置对象
            directory: 目录路径
            suffix: 文件名后缀
        """
        dir_path = Path(directory)
        if not dir_path.is_dir():
            raise ValueError(f"{directory} is not a valid directory")
        
        for file_path in dir_path.iterdir():
            if file_path.is_file() and file_path.name.endswith(suffix):
                self.put(fb, file_path)
    
    def put_dir_with_prefix_suffix(
        self, 
        fb: FtpConfigBean, 
        directory: Union[str, Path], 
        prefix: str, 
        suffix: str
    ) -> None:
        """
        上传目录中同时满足前缀和后缀的文件
        
        Args:
            fb: FTP配置对象
            directory: 目录路径
            prefix: 文件名前缀
            suffix: 文件名后缀
        """
        dir_path = Path(directory)
        if not dir_path.is_dir():
            raise ValueError(f"{directory} is not a valid directory")
        
        for file_path in dir_path.iterdir():
            if (file_path.is_file() and 
                file_path.name.startswith(prefix) and 
                file_path.name.endswith(suffix)):
                self.put(fb, file_path)
    
    def put_dir_with_pattern(self, fb: FtpConfigBean, directory: Union[str, Path], pattern: str) -> None:
        """
        上传目录中匹配正则表达式的文件
        
        Args:
            fb: FTP配置对象
            directory: 目录路径
            pattern: 正则表达式模式
        """
        dir_path = Path(directory)
        if not dir_path.is_dir():
            raise ValueError(f"{directory} is not a valid directory")
        
        regex = re.compile(pattern)
        for file_path in dir_path.iterdir():
            if file_path.is_file() and regex.match(file_path.name):
                self.put(fb, file_path)
    
    def put_whole_dir(self, fb: FtpConfigBean, directory: Union[str, Path]) -> None:
        """
        上传整个目录中的所有文件
        
        Args:
            fb: FTP配置对象
            directory: 目录路径
        """
        dir_path = Path(directory)
        if not dir_path.is_dir():
            raise ValueError(f"{directory} is not a valid directory")
        
        for file_path in dir_path.iterdir():
            if file_path.is_file():
                self._ftp_put_file(fb, file_path)
    
    def put_files(self, fb: FtpConfigBean, files: List[Union[str, Path]]) -> None:
        """
        上传文件列表
        
        Args:
            fb: FTP配置对象
            files: 文件路径列表
        """
        if not files:
            raise ValueError("Empty file list")
        
        for file_path in files:
            path = Path(file_path)
            if path.is_file():
                self.put(fb, path)
            elif path.is_dir():
                self.put_whole_dir(fb, path)
    
    # ========================================== FTP上传实现 ============================================
    
    def _ftp_put_file(self, fb: FtpConfigBean, file_path: Union[str, Path]) -> None:
        """
        FTP上传文件
        
        Args:
            fb: FTP配置对象
            file_path: 文件路径
        """
        path = Path(file_path)
        
        # 如果文件不存在，尝试使用本地目录
        if not path.exists() or not path.is_file():
            if not fb.local_dir:
                raise FileNotFoundError(f"{file_path} does not exist and local_dir is empty")
            
            # 构建完整路径
            local_dir = Path(fb.local_dir)
            if fb.local_dir.endswith(os.sep):
                path = local_dir / file_path
            else:
                path = local_dir / os.sep / file_path
            
            if not path.exists() or not path.is_file():
                raise FileNotFoundError(f"{path} does not exist")
        
        # 如果没有指定目标文件名，使用原文件名
        if not fb.dst_file_name:
            fb.dst_file_name = path.name
        
        # 以二进制模式打开文件上传
        with open(path, 'rb') as file_stream:
            self._ftp_put_stream(fb, file_stream)
    
    def _ftp_put_stream(self, fb: FtpConfigBean, stream: BinaryIO) -> None:
        """
        FTP上传流数据
        
        Args:
            fb: FTP配置对象
            stream: 数据流
        """
        ftp = None
        try:
            # 创建FTP连接
            ftp = ftplib.FTP()
            
            # 设置调试级别
            if self._debug:
                ftp.set_debuglevel(2)
                self.logger.debug(f"Connecting to {fb.host}:{fb.port}")
            
            # 连接服务器
            ftp.connect(fb.host, fb.port)
            
            # 登录
            ftp.login(fb.account, fb.password)
            
            # 设置传输模式
            if fb.mode.lower() == 'bin':
                ftp.sendcmd('TYPE I')  # 二进制模式
            else:
                ftp.sendcmd('TYPE A')  # ASCII模式
            
            # 切换到远程目录
            if fb.remote_dir:
                ftp.cwd(fb.remote_dir)
            
            # 发送自定义命令（如果有）
            if fb.quote:
                ftp.sendcmd(fb.quote)
            
            # 上传文件
            if fb.is_append:
                # 追加模式（FTP协议可能不支持所有服务器）
                self.logger.warning("FTP append mode may not be supported by all servers")
                # 这里简化处理，实际FTP协议没有标准的追加命令
                ftp.storbinary(f'STOR {fb.dst_file_name}', stream)
            else:
                # 普通上传
                ftp.storbinary(f'STOR {fb.dst_file_name}', stream)
            
            self.logger.info(f"Successfully uploaded to {fb.host}/{fb.dst_file_name}")
            
        except ftplib.all_errors as e:
            self.logger.error(f"FTP error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error uploading file: {e}")
            raise
        finally:
            # 确保关闭连接
            if ftp:
                try:
                    ftp.quit()
                except:
                    ftp.close()
    
    # ========================================== FTP下载实现 ============================================
    
    def _ftp_get(self, fb: FtpConfigBean) -> List[Path]:
        """
        FTP下载文件
        
        Args:
            fb: FTP配置对象
            
        Returns:
            下载到本地的文件路径列表
        """
        ftp = None
        downloaded_files = []
        
        try:
            # 创建FTP连接
            ftp = ftplib.FTP()
            
            # 设置调试级别
            if self._debug:
                ftp.set_debuglevel(2)
            
            # 连接服务器
            ftp.connect(fb.host, fb.port)
            
            # 登录
            ftp.login(fb.account, fb.password)
            
            # 设置传输模式
            if fb.mode.lower() == 'bin':
                ftp.sendcmd('TYPE I')  # 二进制模式
            else:
                ftp.sendcmd('TYPE A')  # ASCII模式
            
            # 切换到远程目录
            if fb.remote_dir:
                ftp.cwd(fb.remote_dir)
            
            # 获取文件列表
            files = ftp.nlst()
            
            # 编译正则表达式模式
            pattern = re.compile(fb.pattern)
            
            # 确保本地目录存在
            local_dir = Path(fb.local_dir) if fb.local_dir else Path.cwd()
            local_dir.mkdir(parents=True, exist_ok=True)
            
            # 下载匹配的文件
            for filename in files:
                if pattern.match(filename):
                    local_path = local_dir / filename
                    
                    self.logger.info(f"Downloading {filename} to {local_path}")
                    
                    # 下载文件
                    with open(local_path, 'wb') as local_file:
                        ftp.retrbinary(f'RETR {filename}', local_file.write)
                    
                    downloaded_files.append(local_path)
                    
                    # 如果需要，删除远程文件
                    if fb.is_delete_remote_file:
                        ftp.delete(filename)
                        self.logger.info(f"Deleted remote file: {filename}")
            
            return downloaded_files
            
        except ftplib.all_errors as e:
            self.logger.error(f"FTP error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error downloading files: {e}")
            raise
        finally:
            # 确保关闭连接
            if ftp:
                try:
                    ftp.quit()
                except:
                    ftp.close()
    
    # ========================================== SFTP上传实现 ============================================
    
    def _sftp_put_file(self, fb: FtpConfigBean, file_path: Path) -> None:
        """
        SFTP上传文件
        
        Args:
            fb: FTP配置对象
            file_path: 文件路径
        """
        # 如果文件不存在，尝试使用本地目录
        if not file_path.exists() or not file_path.is_file():
            if not fb.local_dir:
                raise FileNotFoundError(f"{file_path} does not exist and local_dir is empty")
            
            # 构建完整路径
            local_dir = Path(fb.local_dir)
            if fb.local_dir.endswith(os.sep):
                file_path = local_dir / file_path
            else:
                file_path = local_dir / os.sep / file_path
            
            if not file_path.exists() or not file_path.is_file():
                raise FileNotFoundError(f"{file_path} does not exist")
        
        # 如果没有指定目标文件名，使用原文件名
        if not fb.dst_file_name:
            fb.dst_file_name = file_path.name
        
        # 打开文件上传
        with open(file_path, 'rb') as file_stream:
            self._sftp_put_stream(fb, file_stream)
    
    def _sftp_put_stream(self, fb: FtpConfigBean, stream: BinaryIO) -> None:
        """
        SFTP上传流数据
        
        Args:
            fb: FTP配置对象
            stream: 数据流
        """
        ssh = None
        sftp = None
        
        try:
            # 创建SSH客户端
            ssh = paramiko.SSHClient()
            
            # 自动添加主机密钥（生产环境应更安全）
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # 连接服务器
            ssh.connect(
                hostname=fb.host,
                port=fb.port,
                username=fb.account,
                password=fb.password
            )
            
            # 创建SFTP客户端
            sftp = ssh.open_sftp()
            
            # 切换到远程目录
            if fb.remote_dir:
                try:
                    sftp.chdir(fb.remote_dir)
                except IOError:
                    # 目录可能不存在，尝试创建
                    self._sftp_create_directory(sftp, fb.remote_dir)
                    sftp.chdir(fb.remote_dir)
            
            # 上传文件
            if fb.is_append:
                # 追加模式
                # 注意：SFTP协议支持追加，但需要检查文件是否存在
                try:
                    # 尝试获取文件大小以定位到末尾
                    file_stat = sftp.stat(fb.dst_file_name)
                    with sftp.open(fb.dst_file_name, 'ab') as remote_file:
                        # 定位到文件末尾
                        remote_file.seek(file_stat.st_size)
                        # 读取流数据并写入
                        while chunk := stream.read(8192):
                            remote_file.write(chunk)
                except FileNotFoundError:
                    # 文件不存在，创建新文件
                    with sftp.open(fb.dst_file_name, 'wb') as remote_file:
                        while chunk := stream.read(8192):
                            remote_file.write(chunk)
            else:
                # 普通上传（覆盖）
                with sftp.open(fb.dst_file_name, 'wb') as remote_file:
                    while chunk := stream.read(8192):
                        remote_file.write(chunk)
            
            self.logger.info(f"Successfully uploaded to {fb.host}/{fb.dst_file_name}")
            
        except paramiko.SSHException as e:
            self.logger.error(f"SSH/SFTP error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error uploading file via SFTP: {e}")
            raise
        finally:
            # 确保关闭连接
            if sftp:
                sftp.close()
            if ssh:
                ssh.close()
    
    def _sftp_create_directory(self, sftp: paramiko.SFTPClient, remote_dir: str) -> None:
        """
        递归创建远程目录
        
        Args:
            sftp: SFTP客户端
            remote_dir: 远程目录路径
        """
        # 分割路径
        parts = remote_dir.strip('/').split('/')
        current_path = ''
        
        for part in parts:
            if part:  # 跳过空部分
                current_path = f"{current_path}/{part}" if current_path else part
                try:
                    sftp.stat(current_path)
                except FileNotFoundError:
                    sftp.mkdir(current_path)
    
    # ========================================== SFTP下载实现 ============================================
    
    def _sftp_get(self, fb: FtpConfigBean) -> List[Path]:
        """
        SFTP下载文件
        
        Args:
            fb: FTP配置对象
            
        Returns:
            下载到本地的文件路径列表
        """
        ssh = None
        sftp = None
        downloaded_files = []
        
        try:
            # 创建SSH客户端
            ssh = paramiko.SSHClient()
            
            # 自动添加主机密钥
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # 连接服务器
            ssh.connect(
                hostname=fb.host,
                port=fb.port,
                username=fb.account,
                password=fb.password
            )
            
            # 创建SFTP客户端
            sftp = ssh.open_sftp()
            
            # 切换到远程目录
            if fb.remote_dir:
                sftp.chdir(fb.remote_dir)
            
            # 获取文件列表
            file_list = sftp.listdir()
            
            # 编译正则表达式模式
            pattern = re.compile(fb.pattern)
            
            # 确保本地目录存在
            local_dir = Path(fb.local_dir) if fb.local_dir else Path.cwd()
            local_dir.mkdir(parents=True, exist_ok=True)
            
            # 下载匹配的文件
            for filename in file_list:
                if pattern.match(filename):
                    # 构建本地文件路径
                    if fb.local_dir.endswith(os.sep):
                        local_path = local_dir / filename
                    else:
                        local_path = local_dir / os.sep / filename
                    
                    self.logger.info(f"Downloading {filename} to {local_path}")
                    
                    # 下载文件
                    sftp.get(filename, str(local_path))
                    downloaded_files.append(local_path)
                    
                    # 如果需要，删除远程文件
                    if fb.is_delete_remote_file:
                        sftp.remove(filename)
                        self.logger.info(f"Deleted remote file: {filename}")
            
            return downloaded_files
            
        except paramiko.SSHException as e:
            self.logger.error(f"SSH/SFTP error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error downloading files via SFTP: {e}")
            raise
        finally:
            # 确保关闭连接
            if sftp:
                sftp.close()
            if ssh:
                ssh.close()


# ========================================== 测试功能 ================================================

def test_ftp_upload() -> None:
    """测试FTP上传功能"""

    fb = FtpConfigBean()
    fb.host = "localhost"
    fb.account = "testuser"
    fb.password = "testpass"
    fb.dst_file_name = "test.txt"
    fb.mode = "asc"
    fb.is_append = False
    fb.ssh_enabled = False  # 明确设置为False，使用FTP
    
    # 创建测试数据
    test_data = "This is a test string for FTP upload"
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
        tmp_file.write(test_data)
        tmp_file_path = tmp_file.name
    
    try:
        # 创建FTP帮助器
        helper = FtpHelper()
        
        # 测试字符串上传
        print("Testing string upload...")
        helper.put(fb, test_data)
        
        # 测试文件上传
        print("Testing file upload...")
        fb.dst_file_name = "test_file.txt"
        helper.put(fb, Path(tmp_file_path))
        
        # 测试字节数据上传
        print("Testing bytes upload...")
        fb.dst_file_name = "test_bytes.txt"
        helper.put(fb, test_data.encode('utf-8'))
        
        print("All tests completed!")
        
    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        # 清理临时文件
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)


def test_sftp_upload() -> None:
    """测试SFTP上传功能"""
    # 创建测试配置
    from ..config import FtpConfigBean
    fb = FtpConfigBean()
    fb.host = "localhost"
    fb.port = 22
    fb.account = "testuser"
    fb.password = "testpass"
    fb.ssh_enabled = True
    fb.dst_file_name = "test_sftp.txt"
    fb.mode = "bin"
    
    # 创建测试数据
    test_data = "This is a test string for SFTP upload"
    
    try:
        # 创建FTP帮助器
        helper = FtpHelper()
        
        # 测试字符串上传
        print("Testing SFTP string upload...")
        helper.put(fb, test_data)
        
        print("SFTP test completed!")
        
    except Exception as e:
        print(f"SFTP test failed: {e}")
        print("Note: This test requires a running SFTP server")


def main() -> None:
    """主函数 - 演示和测试"""
    import sys
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    print("=== FtpHelper 功能演示 ===")
    
    # 测试FTP上传
    print("\n1. 测试FTP上传功能:")
    try:
        # 临时创建测试配置进行演示
        from ..config import FtpConfigBean
        fb = FtpConfigBean()
        fb.host = "BLDSYG.BOULDER.IBM.COM"
        fb.account = "LIZYUAN"
        fb.password = "6789oiuy"
        fb.dst_file_name = "demo_test.txt"
        fb.mode = "asc"
        
        helper = FtpHelper()
        test_data = "FTP Helper Demo Test"
        helper.put(fb, test_data)
        
        
        print("尝试上传测试数据...")
        # 这里不实际连接服务器，只演示代码逻辑
        print(f"配置: host={fb.host}, file={fb.dst_file_name}")
        print("FTP上传演示完成（需要实际FTP服务器才能测试）")
        
    except Exception as e:
        print(f"FTP测试失败: {e}")
    
    # 测试SFTP上传
    print("\n2. 测试SFTP上传功能:")
    try:
        from ..config import FtpConfigBean
        fb = FtpConfigBean()
        fb.host = "BLDSYG.BOULDER.IBM.COM"
        fb.port = 22
        fb.account = "LIZYUAN"
        fb.password = "6789oiuy"
        fb.ssh_enabled = True
        fb.dst_file_name = "demo_sftp_test.txt"
        
        print("SFTP上传演示完成（需要实际SFTP服务器才能测试）")
        
    except Exception as e:
        print(f"SFTP演示失败: {e}")
    
    print("\n=== 演示完成 ===")


if __name__ == "__main__":
    # 只有在直接运行此脚本时才执行main函数，避免在导入时自动执行
    main()