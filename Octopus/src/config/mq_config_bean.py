# mq_config_bean.py
"""
MQ配置bean，采用Pythonic接口。
"""

from typing import List, Optional,TYPE_CHECKING, Any
from .common_config_bean import CommonConfigBean


if TYPE_CHECKING:
    pass

class MqConfigBean(CommonConfigBean):
    """
    MQ参数配置bean。
    """
    
    def __init__(self):
        """使用默认值初始化MqConfigBean。"""
        super().__init__()
        self._host: Optional[str] = None
        self._port: int = 1414
        self._account: Optional[str] = None
        self._password: Optional[str] = None
        self._qm: Optional[str] = None
        self._channel: Optional[str] = None
        self._q: Optional[str] = None
        self._message: Optional[str] = None

    def validate(self) -> None:
        """
        验证必需字段。
        
        抛出异常:
            Exception: 如果必需字段为空。
        """
        if not self._qm:
            raise Exception(f"P08000:'qm' is empty in '{self.name}'.")
        if not self._q:
            raise Exception(f"P08001:'q' is empty in '{self.name}'.")
        if not self._channel:
            raise Exception(f"P08002:'channel' is empty in '{self.name}'.")

    def do_extend(self, config_lists: List[List['MqConfigBean']]) -> None:
        """
        检查是否需要扩展，
        如果需要扩展，则在config_lists中查找父元素
        并从中扩展属性。
        
        重要说明：继承规则。对象只能从同级或更高级别的对象继承。
        
        参数:
            config_lists: 要搜索父级的MQ配置bean列表。
            
        抛出异常:
            Exception: 如果未找到父级或在扩展链中存在死循环。
        """
        if not self.extend or not self.name:
            return
            
        if self.extend.lower() == self.name.lower():
            raise Exception("dead loop on extends chains")
        
        # 从高层级向低层级搜索
        for config_list in reversed(config_lists):
            for config in config_list:
                if self.extend.lower() == config.name.lower():
                    self._extend_from(config)
                    self.do_extend(config_lists)
                    return
                    
        raise Exception(f"There is no parent found for name->{self.name} and extend->{self.extend}.")

    def _extend_from(self, other: 'MqConfigBean') -> None:
        """
        从另一个MqConfigBean扩展属性。
        
        参数:
            other: 要从中扩展的MqConfigBean。
        """
        if not self.name:
            self.name = other.name
        self.extend = other.extend
        if not self._host:
            self._host = other.host
        if self._port == 1414:
            self._port = other.port
        if not self._account:
            self._account = other.account
        if not self._password:
            self._password = other.password
        if not self._qm:
            self._qm = other.qm
        if not self._q:
            self._q = other.q
        if not self._channel:
            self._channel = other.channel
        if not self._message:
            self._message = other.message

    def copy(self) -> 'MqConfigBean':
        """
        克隆具有相同属性的bean。
        
        返回:
            MqConfigBean: 具有相同属性的新实例。
        """
        # 获取父类副本
        parent_copy = super().copy()
        
        # 创建新实例
        bean = MqConfigBean()
        
        # 复制父类属性
        bean._name = parent_copy._name
        bean._id = parent_copy._id
        bean._extend = parent_copy._extend
        bean._mqs = parent_copy._mqs.copy()
        bean._ftps = parent_copy._ftps.copy()
        bean._emails = parent_copy._emails.copy()
        bean._files = parent_copy._files.copy()
        
        # 复制MQ特定属性
        bean._host = self._host
        bean._port = self._port
        bean._account = self._account
        bean._password = self._password
        bean._qm = self._qm
        bean._channel = self._channel
        bean._q = self._q
        bean._message = self._message
        
        return bean

    # --- 属性方法 ---

    @property
    def host(self) -> str:
        """
        获取MQ主机。
        
        返回:
            str: 主机，如果未设置则返回'localhost'。
        """
        if not self._host or not self._host.strip():
            return "localhost"
        return self._host

    @host.setter
    def host(self, value: str) -> None:
        """
        设置MQ主机。
        
        参数:
            value (str): 要设置的主机。
        """
        self._host = value

    @property
    def port(self) -> int:
        """
        获取MQ端口。
        
        返回:
            int: 端口号。
        """
        return self._port

    @port.setter
    def port(self, value: int) -> None:
        """
        设置MQ端口。
        
        参数:
            value (int): 要设置的端口。
        """
        self._port = value

    @property
    def account(self) -> Optional[str]:
        """
        获取MQ账户。
        
        返回:
            str: 账户。
        """
        return self._account

    @account.setter
    def account(self, value: str) -> None:
        """
        设置MQ账户。
        
        参数:
            value (str): 要设置的账户。
        """
        self._account = value

    @property
    def password(self) -> Optional[str]:
        """
        获取MQ密码。
        
        返回:
            str: 密码。
        """
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        """
        设置MQ密码。
        
        参数:
            value (str): 要设置的密码。
        """
        self._password = value

    @property
    def qm(self) -> Optional[str]:
        """
        获取MQ队列管理器名称。
        
        返回:
            str: 队列管理器名称。
        """
        return self._qm

    @qm.setter
    def qm(self, value: str) -> None:
        """
        设置MQ队列管理器名称。
        
        参数:
            value (str): 要设置的队列管理器名称。
        """
        self._qm = value

    @property
    def channel(self) -> Optional[str]:
        """
        获取MQ通道。
        
        返回:
            str: 通道。
        """
        return self._channel

    @channel.setter
    def channel(self, value: str) -> None:
        """
        设置MQ通道。
        
        参数:
            value (str): 要设置的通道。
        """
        self._channel = value

    @property
    def q(self) -> Optional[str]:
        """
        获取MQ队列名称。
        
        返回:
            str: 队列名称。
        """
        return self._q

    @q.setter
    def q(self, value: str) -> None:
        """
        设置MQ队列名称。
        
        参数:
            value (str): 要设置的队列名称。
        """
        self._q = value

    @property
    def message(self) -> Optional[str]:
        """
        获取MQ消息。
        
        返回:
            str: 消息。
        """
        return self._message

    @message.setter
    def message(self, value: str) -> None:
        """
        设置MQ消息。
        
        参数:
            value (str): 要设置的消息。
        """
        self._message = value

    def __str__(self) -> str:
        """
        返回MQ配置的字符串表示。
        
        返回:
            str: 字符串表示。
        """
        lines = [
            "--------------- mq config ---------------",
            super().__str__(),
            f"host : {self._host}",
            f"port : {self._port}",
            f"account : {self._account}",
            f"password : {self._password}",
            f"qm : {self._qm}",
            f"channel : {self._channel}",
            f"q : {self._q}"
        ]
        return "\n".join(lines)

if __name__ == "__main__":
    # 测试代码
    config = MqConfigBean()
    config.name = "test_config"
    config.qm = "QM1"
    config.q = "TEST.QUEUE"
    config.channel = "SYSTEM.DEF.SVRCONN"

    extend1 = MqConfigBean()
    extend1.name = "test_config1"
    extend1.extend = "test_config"
    extend1.q = 'TEST.QUEUE.1'
    extend1.qm = "QM2"
    extend1.channel = "SYSTEM.DEF.SVRCONN2"
    
    try:
        extend1.validate()
        print("配置验证通过")
    except Exception as e:
        print(f"配置验证失败: {e}")
    
    print(extend1)