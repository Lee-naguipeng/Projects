# send_msg_config_bean.py

from typing import Optional
from .email_config_bean import EmailConfigBean
from .mq_config_bean import MqConfigBean


class SendMsgConfigBean:
    """
    发送消息的配置bean。
    """
    
    def __init__(self):
        """使用默认值初始化SendMsgConfigBean。"""
        self._is_send_email: bool = False
        self._email_conf: Optional['EmailConfigBean'] = None
        self._is_send_mq: bool = False
        self._mq_conf: Optional['MqConfigBean'] = None

    @property
    def is_send_email(self) -> bool:
        """
        获取是否发送电子邮件消息。
        
        返回:
            bool: 如果应发送电子邮件则返回True，否则返回False。
        """
        return self._is_send_email

    @is_send_email.setter
    def is_send_email(self, value: bool) -> None:
        """
        设置是否发送电子邮件消息。
        
        参数:
            value (bool): 如果要发送电子邮件则为True，否则为False。
        """
        self._is_send_email = value

    @property
    def email_conf(self) -> Optional['EmailConfigBean']:
        """
        获取电子邮件配置。
        
        返回:
            EmailConfigBean: 电子邮件配置对象。
        """
        return self._email_conf

    @email_conf.setter
    def email_conf(self, value: Optional['EmailConfigBean']) -> None:
        """
        设置电子邮件配置。
        
        参数:
            value (EmailConfigBean): 电子邮件配置对象。
        """
        self._email_conf = value

    @property
    def is_send_mq(self) -> bool:
        """
        获取是否发送MQ消息。
        
        返回:
            bool: 如果应发送MQ消息则返回True，否则返回False。
        """
        return self._is_send_mq

    @is_send_mq.setter
    def is_send_mq(self, value: bool) -> None:
        """
        设置是否发送MQ消息。
        
        参数:
            value (bool): 如果要发送MQ消息则为True，否则为False。
        """
        self._is_send_mq = value

    @property
    def mq_conf(self) -> Optional['MqConfigBean']:
        """
        获取MQ配置。
        
        返回:
            MqConfigBean: MQ配置对象。
        """
        return self._mq_conf

    @mq_conf.setter
    def mq_conf(self, value: Optional['MqConfigBean']) -> None:
        """
        设置MQ配置。
        
        参数:
            value (MqConfigBean): MQ配置对象。
        """
        self._mq_conf = value

    def __str__(self) -> str:
        """
        将此对象转换为字符串。
        
        返回:
            str: 对象的字符串表示形式。
        """
        buffer = []
        
        if self._email_conf is not None:
            buffer.append(str(self._email_conf))
        if self._mq_conf is not None:
            buffer.append(str(self._mq_conf))
            
        return "".join(buffer)

if __name__ == "__main__":
    # Test each method
    Send_config = SendMsgConfigBean()
    Send_config.mq_conf=MqConfigBean()
    Send_config.email_conf=EmailConfigBean()
    print (Send_config)
