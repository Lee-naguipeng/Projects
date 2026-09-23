# http_config_bean.py

from typing import List, Optional
from urllib.parse import urlparse


class HttpConfigBean:
    """HTTP 配置类"""

    def __init__(self):
        self._is_ssl_debug = False
        self._url: Optional[str] = None
        self._protocol: Optional[str] = None
        self._host: Optional[str] = None
        self._port = -1
        self._address: Optional[str] = None
        self._is_auth = False
        self._username: Optional[str] = None
        self._password: Optional[str] = None
        self._key_store: Optional[str] = None
        self._key_store_password: Optional[str] = None
        self._trust_store: Optional[str] = None
        self._trust_store_password: Optional[str] = None
        self._parameters: List[str] = []

    @property
    def is_ssl_debug(self) -> bool:
        return self._is_ssl_debug

    @is_ssl_debug.setter
    def is_ssl_debug(self, value: bool):
        self._is_ssl_debug = value

    @property
    def url(self) -> Optional[str]:
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value

    @property
    def protocol(self) -> Optional[str]:
        if self._protocol is not None:
            return self._protocol
        
        if self._url is not None:
            url_lower = self._url.lower()
            if url_lower.startswith("https"):
                return "https"
            if url_lower.startswith("http"):
                return "http"
        
        return self._protocol

    @protocol.setter
    def protocol(self, value: str):
        self._protocol = value

    @property
    def host(self) -> str:
        if self._host is None and self._url is not None:
            try:
                parsed_url = urlparse(self.url)
                self._host = parsed_url.hostname
            except Exception as e:
                print(f"Error parsing URL: {e}")
        
        return self._host if self._host is not None else ""

    @host.setter
    def host(self, value: str):
        self._host = value

    @property
    def port(self) -> int:
        if self._port != -1:
            return self._port
        
        protocol = self.protocol
        if protocol and protocol.lower() == "http":
            return 80
        if protocol and protocol.lower() == "https":
            return 443
        
        return self._port

    @port.setter
    def port(self, value: int):
        self._port = value

    @property
    def address(self) -> Optional[str]:
        return self._address

    @address.setter
    def address(self, value: str):
        self._address = value

    @property
    def is_auth(self) -> bool:
        return self._is_auth

    @is_auth.setter
    def is_auth(self, value: bool):
        self._is_auth = value

    @property
    def username(self) -> Optional[str]:
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value

    @property
    def password(self) -> Optional[str]:
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value

    @property
    def key_store(self) -> Optional[str]:
        return self._key_store

    @key_store.setter
    def key_store(self, value: str):
        self._key_store = value

    @property
    def key_store_password(self) -> Optional[str]:
        return self._key_store_password

    @key_store_password.setter
    def key_store_password(self, value: str):
        self._key_store_password = value

    @property
    def trust_store(self) -> Optional[str]:
        return self._trust_store

    @trust_store.setter
    def trust_store(self, value: str):
        self._trust_store = value

    @property
    def trust_store_password(self) -> Optional[str]:
        return self._trust_store_password

    @trust_store_password.setter
    def trust_store_password(self, value: str):
        self._trust_store_password = value

    @property
    def parameters(self) -> List[str]:
        return self._parameters.copy()

    @parameters.setter
    def parameters(self, value: List[str]):
        self._parameters = value.copy() if value is not None else []

    def add_parameter(self, parameter: str):
        """添加参数到参数列表"""
        self._parameters.append(parameter)

    def __str__(self) -> str:
        result = ["----------------------------http config--------------------------"]
        result.append(f"url->{self._url}")
        result.append(f"protocol->{self._protocol}")
        result.append(f"port->{self._port}")
        result.append(f"address->{self._address}")
        result.append(f"is_auth->{self._is_auth}")
        result.append(f"username->{self._username}")
        result.append(f"password->{self._password}")
        result.append(f"trust_store->{self._trust_store}")
        result.append(f"trust_store_password->{self._trust_store_password}")
        result.append(f"key_store->{self._key_store}")
        result.append(f"key_store_password->{self._key_store_password}")
        
        for i, param in enumerate(self._parameters):
            result.append(f"parameter {i}->{param}")
        
        return "\n".join(result)


if __name__ == "__main__":
    # 测试代码
    config = HttpConfigBean()
    config.url = 'www.baidu.com'
    config.port= 8080
    config.parameters=['parm1','parm2']
    print(config)