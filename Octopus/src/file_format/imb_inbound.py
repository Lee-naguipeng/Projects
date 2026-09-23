# imb_inbound.py

import logging
from typing import List, Optional
from io import StringIO
from config.imb_config_bean import IMBConfigBean
from helper.string_helper import StringHelper


class IMBDRecord:
    """
    IMB D记录类
    
    它会在第5个字段后截断数据文件记录。每个字段使用分隔符(|)标识并保留。
    第二个字段左对齐并用空格填充至15字节。
    然后在每条记录前追加4字符的记录长度和"D"值。
    因此每条记录在截断其他数据字段后应该是固定宽度70字节。
    0067D!xxx!xxxxxxxxxxxxxxx!xxx!xxxxxxxxxxxxxxxxxxx!xxxxxxxxxxxxxxxxxxx!
    """

    def __init__(self, record_str: str) -> None:
        """
        从字符串构造IMBDRecord对象
        
        Args:
            record_str: 代表记录的字符串
            
        Raises:
            Exception: 当输入字符串为空或字段数少于5时抛出异常
        """
        if record_str is None:
            raise Exception("无法从空字符串构造IMBDRecord")
        
        fields = record_str.split('|')
        if len(fields) < 5:
            raise Exception("IMB D记录格式错误，字段数少于5个")
        
        buffer = ["0070D|"]
        for i in range(5):
            field = fields[i]
            if i == 1:
                buffer.append(StringHelper.right_fill(field, 15, 32) + "|")
            else:
                buffer.append(field + "|")
        
        self.record = "".join(buffer)

    def __str__(self) -> str:
        return self.record


class IMBInbound:
    """
    IMB入站文件处理类
    """

    def __init__(self, inbound_data: Optional[bytes] = None, 
                 config: Optional[IMBConfigBean] = None,
                 logger: Optional[logging.Logger] = None) -> None:
        """
        构造IMBInbound对象
        
        Args:
            inbound_data: 待解析的字节数组
            config: 配置bean
            logger: 日志记录器
        """
        self.inbound_data: Optional[bytes] = inbound_data
        self.config: Optional[IMBConfigBean] = config
        self.logger: logging.Logger = logger or logging.getLogger(__name__)
        self.d_records: List[IMBDRecord] = []
        self.m_record: str = ""
        self.a_record: str = ""
        
        if inbound_data is not None and config is not None:
            self.parse()

    def parse(self) -> None:
        """
        解析入站数据
        
        应该包含多行D记录。
        对于每一行，使用'|'分隔成字段。
        保留前5个字段和分隔符。
        在前面添加'LineHeader'，包括4字节记录长度和'D'。
        将第二个字段格式化为左对齐并用空格填充至15字节。
        执行完所有行后，生成M记录和A记录。
        """
        if self.inbound_data is None:
            return
            
        data_str = self.inbound_data.decode('utf-8')
        self.d_records = []
        
        for line in StringIO(data_str):
            line = line.strip()
            if not line:
                continue
            try:
                record = IMBDRecord(line)
                self.d_records.append(record)
            except Exception as e:
                self.logger.error(str(e))
                continue
        
        if self.config:
            self._generate_m_record(self.config)
            self._generate_a_record(len(self.d_records))

    def _generate_m_record(self, config: IMBConfigBean) -> None:
        """
        生成M记录
        
        M记录是固定宽度304字节的记录，由4字符长度和300字节数据组成。
        有5个不同的变量需要从config.xml读取:
        0304Meeeeeeeeccciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxllllllllllllllllbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
        0304M 是5字节常量
        e = <imbMEyeCatch> 左对齐并用空格填充至8字符，称为Eyecatcher
        c = <imbMIopuCty> 左对齐并用空格填充至3字符，称为国家代码
        i = <imbMTpId_To> 左对齐并用空格填充至35字符，称为IMB布局
        x = <imbMTpId_From> 左对齐并用空格填充至35字符，称为IMB到贸易伙伴
        l = <imbMLayout> 左对齐并用空格填充至16字符，称为IMB来自贸易伙伴
        b = 202个空格用于填充记录至总长度304字节
        
        Args:
            config: 包含配置的IMBConfigBean
            
        Raises:
            Exception: 当配置为空或必要配置项缺失时抛出异常
        """
        if config is None:
            raise Exception("IMB配置为空")
            
        buffer = ["0304M"]
        
        if config.imb_m_eye_catch is None:
            raise Exception("imb->imbMEyeCatch为空")
        buffer.append(StringHelper.right_fill(config.imb_m_eye_catch, 8, 32))
        
        if config.imb_m_iopu_cty is None:
            raise Exception("imb->imbMIopuCty为空")
        buffer.append(StringHelper.right_fill(config.imb_m_iopu_cty, 3, 32))
        
        if config.imb_m_tp_id_to is None:
            raise Exception("imb->imbMTpId_To为空")
        buffer.append(StringHelper.right_fill(config.imb_m_tp_id_to, 35, 32))
        
        if config.imb_m_tp_id_from is None:
            raise Exception("imb->imbMTpId_From为空")
        buffer.append(StringHelper.right_fill(config.imb_m_tp_id_from, 35, 32))
        
        if config.imb_m_layout is None:
            raise Exception("imb->imbMLayout为空")
        buffer.append(StringHelper.right_fill(config.imb_m_layout, 16, 32))
        
        buffer.append(StringHelper.right_fill("", 202, 32))
        self.m_record = "".join(buffer)

    def _generate_a_record(self, d_record_count: int) -> None:
        """
        生成A记录
        
        A记录是固定宽度100字节。其中唯一的变量是D记录的数量。
        其他都是常量:
        APbbbbbbbb########bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
        "AP" 是2字节常量
        b = 8个空格
        # = 上述创建的D记录数量，右对齐，用零填充至8字节
        b = 82个空格用于填充至100字节长度
        
        Args:
            d_record_count: D记录的数量
        """
        buffer = ["AP"]
        buffer.append(StringHelper.left_fill("", 8, 32))
        # 由caishu@cn.ibm.com修订，将M记录包含在记录计数中
        buffer.append(StringHelper.left_fill(d_record_count + 1, 8, 48))
        buffer.append(StringHelper.left_fill("", 82, 32))
        self.a_record = "".join(buffer)

    def __str__(self) -> str:
        """
        创建IMB字符串表示
        
        Returns:
            str: IMB消息的字符串表示
        """
        lines = [self.a_record, self.m_record]
        for i, record in enumerate(self.d_records):
            lines.append(str(record))
        return "\n".join(lines)

    # 测试方法可以另外实现