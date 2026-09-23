"""
基于 Apache Commons Digester 的 XML 配置文件解析器
"""

import os
import sys
from typing import Optional, Dict, List, Any, Union
from xml.etree import ElementTree as ET
from pathlib import Path

# Import configuration classes
from .tps_config_bean import TPsConfigBean
from .tp_config_bean import TPConfigBean
from .controller_config_bean import ControllerConfigBean
from .interface_config_bean import InterfaceConfigBean
from .mq_config_bean import MqConfigBean
from .ftp_config_bean import FtpConfigBean
from .http_config_bean import HttpConfigBean
from .email_config_bean import EmailConfigBean
from .file_config_bean import FileConfigBean
from .filter_config_bean import FilterConfigBean
from .send_msg_config_bean import SendMsgConfigBean


class MyParser:
    """
    配置文件解析器
    对应 Java 的 MyParser 类，用于解析 XML 配置文件
    
    属性:
        rules: 解析规则字典
        context: 解析上下文
    """
    
    def __init__(self, rules_engine=None):
        """
        初始化解析器
        
        Args:
            rules_engine: 可选的规则引擎（Python 中没有 Digester 的直接对应）
        """
        self.rules_engine = rules_engine
        self._rules: Dict[str, List[Any]] = {}
        self._context: Dict[str, Any] = {}
    
    def prepare_parse_mq(self):
        """准备解析 MQ 配置"""
        print("Preparing to parse MQ configuration...")
        # 在实际实现中，这里会设置 MQ 相关的解析规则
        pass
    
    def prepare_parse_ftp(self):
        """准备解析 FTP 配置"""
        print("Preparing to parse FTP configuration...")
        # 在实际实现中，这里会设置 FTP 相关的解析规则
        pass
    
    def prepare_parse(self):
        """
        准备解析完整的交易伙伴配置
        对应 Java 中的 prepareParse() 方法
        """
        print("Preparing to parse trading partners configuration...")
        # 设置交易伙伴配置的解析规则
        # 在实际实现中，这里会调用各种 execute_xxx 方法设置规则
        self._execute_trading_partner_config_bean("tradingPartners/", True)
    
    def _execute_trading_partner_config_bean(self, prefix: str, is_next: bool):
        """
        执行交易伙伴配置 Bean 的解析规则
        对应 Java 中的 executeTradingPartnerConfigBean 方法
        """
        print(f"Executing trading partner configuration parsing rules: prefix={prefix}, is_next={is_next}")
        # 实际规则设置逻辑
    
    def _execute_interface_config_bean(self, prefix: str, is_next: bool):
        """
        执行接口配置 Bean 的解析规则
        对应 Java 中的 executeInterfaceConfigBean 方法
        """
        print(f"Executing interface configuration parsing rules: prefix={prefix}, is_next={is_next}")
        # 实际规则设置逻辑
    
    def _exec_common_config_bean(self, prefix: str):
        """
        执行通用配置 Bean 的解析规则
        对应 Java 中的 execCommonConfigBean 方法
        """
        print(f"Executing common configuration parsing rules: prefix={prefix}")
        # 实际规则设置逻辑
    
    def _execute_mq_config_bean(self, prefix: str, method: str):
        """
        执行 MQ 配置 Bean 的解析规则
        对应 Java 中的 executeMqConfigBean 方法
        """
        print(f"Executing MQ configuration parsing rules: prefix={prefix}, method={method}")
        # 实际规则设置逻辑
    
    def _execute_ftp_config_bean(self, prefix: str, method: str):
        """
        执行 FTP 配置 Bean 的解析规则
        对应 Java 中的 executeFtpConfigBean 方法
        """
        print(f"Executing FTP configuration parsing rules: prefix={prefix}, method={method}")
        # 实际规则设置逻辑
    
    def parse_xml(self, xml_file: Union[str, Path]) -> Optional[Any]:
        """
        解析 XML 文件
        对应 Java 中通过 Digester 解析 XML 的功能
        
        Args:
            xml_file: XML 文件路径
            
        Returns:
            解析后的配置对象
        """
        try:
            tree = ET.parse(str(xml_file))
            root = tree.getroot()
            
            # 根据根元素决定如何解析
            if root.tag == "tradingPartners":
                return self._parse_trading_partners(root)
            elif root.tag == "interface":
                return self._parse_interface(root)
            else:
                print(f"Unsupported root element: {root.tag}")
                return None
                
        except Exception as e:
            print(f"Error parsing XML file: {e}", file=sys.stderr)
            return None
    
    def _parse_trading_partners(self, element: ET.Element) -> TPsConfigBean:
        """解析交易伙伴配置"""
        config = TPsConfigBean()
        
        # 遍历子元素并设置属性
        for child in element:
            if child.tag == "workDir":
                config.work_dir = child.text or ""
            elif child.tag == "backupDir":
                config.backup_dir = child.text or ""
            elif child.tag == "tmpDir":
                config.tmp_dir = child.text or ""
            elif child.tag == "name":
                config.name = child.text or ""
            elif child.tag == "tradingPartner":
                partner = self._parse_trading_partner(child)
                config.add_partner(partner)
            elif child.tag == "controller":
                controller = self._parse_controller(child)
                config.add_controller(controller)
            elif child.tag == "mqConf":
                mq_configs = self._parse_mq_configs(child)
                for mq in mq_configs:
                    config.add_mq(mq)
        
        return config
    
    def _parse_trading_partner(self, element: ET.Element) -> TPConfigBean:
        """解析单个交易伙伴配置"""
        partner = TPConfigBean()
        
        for child in element:
            if child.tag == "name":
                partner.name = child.text or ""
            elif child.tag == "isStandAlone":
                partner.is_standalone = child.text.lower() == "true" if child.text else False
            elif child.tag == "className":
                partner.class_name = child.text or ""
            elif child.tag == "controllerName":
                partner.controller_name = child.text or ""
            elif child.tag == "interface":
                interface = self._parse_interface(child)
                if hasattr(partner, "add_interface"):
                    partner.add_interface(interface)
        
        return partner
    
    def _parse_interface(self, element: ET.Element) -> InterfaceConfigBean:
        """解析接口配置"""
        interface = InterfaceConfigBean()
        
        for child in element:
            if child.tag == "name":
                interface.name = child.text or ""
            elif child.tag == "transferClass":
                interface.transfer_class = child.text
            elif child.tag == "dataType":
                interface.data_type = child.text
            elif child.tag == "type":
                interface.type = child.text
            elif child.tag == "contentType":
                interface.content_type = child.text
            elif child.tag == "limitedSize":
                if child.text:
                    interface.limited_size = int(child.text)
            elif child.tag == "mqConf":
                mq_configs = self._parse_mq_configs(child)
                for mq in mq_configs:
                    interface.add_mq(mq)
        
        return interface
    
    def _parse_controller(self, element: ET.Element) -> ControllerConfigBean:
        """解析控制器配置"""
        controller = ControllerConfigBean()
        
        for child in element:
            if child.tag == "name":
                controller.name = child.text or ""
            elif child.tag == "isAllTP":
                controller.is_all_tp = child.text.lower() == "true" if child.text else False
            elif child.tag == "processType":
                controller.process_type = child.text or ""
        
        return controller
    
    def _parse_mq_configs(self, element: ET.Element) -> List[MqConfigBean]:
        """解析 MQ 配置列表"""
        mq_configs = []
        
        for child in element:
            if child.tag == "mqConf":
                mq = MqConfigBean()
                for mq_child in child:
                    if mq_child.tag == "name":
                        mq.name = mq_child.text or ""
                    elif mq_child.tag == "host":
                        mq.host = mq_child.text or ""
                    elif mq_child.tag == "port":
                        if mq_child.text:
                            mq.port = int(mq_child.text)
                    elif mq_child.tag == "qm":
                        mq.queue_manager = mq_child.text or ""
                    elif mq_child.tag == "channel":
                        mq.channel = mq_child.text or ""
                    elif mq_child.tag == "q":
                        mq.queue = mq_child.text or ""
                mq_configs.append(mq)
        
        return mq_configs
    
    @staticmethod
    def main():
        """
        主方法，对应 Java 中的 main 方法
        用于测试解析器功能
        """
        print("=" * 60)
        print("MyParser Test")
        print("=" * 60)
        
        # Sample XML configuration
        sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
<tradingPartners>
    <name>Test Configuration</name>
    <workDir>/app/work</workDir>
    <backupDir>/app/backup</backupDir>
    <tmpDir>/app/tmp</tmpDir>
    
    <tradingPartner>
        <name>Test Partner</name>
        <isStandAlone>true</isStandAlone>
        <className>com.example.TestProcessor</className>
        
        <interface>
            <name>Test Interface</name>
            <transferClass>com.example.Transfer</transferClass>
            <dataType>xml</dataType>
        </interface>
    </tradingPartner>
</tradingPartners>
"""
        
        # Create temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write(sample_xml)
            temp_file = f.name
        
        try:
            # Create parser and parse
            parser = MyParser()
            parser.prepare_parse()  # Prepare parsing rules
            
            # Parse XML
            config = parser.parse_xml(temp_file)
            
            if config:
                print("Parsing successful!")
                print(f"Configuration name: {config.name}")
                print(f"Work directory: {config.work_dir}")
                print(f"Number of partners: {len(config.partners)}")
                
                if config.partners:
                    partner = config.partners[0]
                    print(f"Partner name: {partner.name}")
                    print(f"Standalone: {partner.is_standalone}")
                    print(f"Processor class: {partner.class_name}")
            
            # Delete temporary file
            os.unlink(temp_file)
            
        except Exception as e:
            print(f"Error during parsing: {e}")
            if 'temp_file' in locals():
                os.unlink(temp_file)


# Usage example
if __name__ == "__main__":
    # Run test
    MyParser.main()