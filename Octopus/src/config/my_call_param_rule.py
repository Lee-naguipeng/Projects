"""
Custom call parameter rule for XML parsing.
This class extends the CallParamRule to handle XML element content collection.
"""

from typing import Optional, List, Any
import xml.sax


class MyCallParamRule:
    """
    Custom call parameter rule for XML parsing.
    
    这个类扩展了CallParamRule，用于处理XML元素内容的收集。
    它可以收集属性值、栈中的值或元素体文本。
    """
    
    def __init__(self, param_index: int = 0):
        """
        初始化规则
        
        Args:
            param_index: 参数在参数数组中的索引位置
        """
        self.param_index = param_index
        self.attribute_name: Optional[str] = None
        self.from_stack = False
        self.stack_index = 0
        self.body_text_stack: List[str] = []
        self.current_element_name: str = ""
    
    def set_attribute_name(self, name: str) -> None:
        """设置要从属性中获取参数的属性名"""
        self.attribute_name = name
    
    def set_from_stack(self, from_stack: bool, stack_index: int = 0) -> None:
        """设置是否从栈中获取参数"""
        self.from_stack = from_stack
        self.stack_index = stack_index
    
    def begin(self, name: str, attributes: xml.sax.xmlreader.AttributesImpl) -> None:
        """
        处理元素开始事件
        
        Args:
            name: 元素名
            attributes: 元素属性
        """
        self.current_element_name = name
        param = None
        
        # 从属性获取参数值
        if self.attribute_name is not None:
            param = attributes.getValue(self.attribute_name)
        # 从栈中获取参数值
        elif self.from_stack:
            # 这里需要访问栈，但Python中没有直接对应的Digester栈
            # 在实际实现中，这里应该访问解析器的上下文栈
            pass
        
        # 如果有参数值，设置到参数数组中
        if param is not None:
            # 在实际实现中，这里应该设置到解析器的参数数组中
            pass
        
        # 初始化body文本栈
        if not self.body_text_stack:
            self.body_text_stack.append(f"<{name}>")
        else:
            self.body_text_stack.append(f"<{name}>")
    
    def body(self, body_text: str) -> None:
        """
        处理元素体文本事件
        
        Args:
            body_text: 元素体文本
        """
        # 如果不是从属性或栈中获取参数，则收集元素体文本
        if self.attribute_name is None and not self.from_stack:
            if not self.body_text_stack:
                self.body_text_stack.append("")
            
            # 处理嵌套元素的情况
            tmp = ""
            temp_stack: List[str] = []
            
            # 将栈内容复制到临时栈
            while self.body_text_stack:
                item = self.body_text_stack.pop()
                temp_stack.append(item)
                
                # 如果遇到标签结束，跳出循环
                if not item.endswith(">"):
                    break
                else:
                    tmp = item + tmp
            
            # 将临时栈内容放回原栈
            while temp_stack:
                self.body_text_stack.append(temp_stack.pop())
            
            # 添加当前文本
            if not self.body_text_stack:
                self.body_text_stack.append(body_text.strip())
            else:
                self.body_text_stack.append(self.body_text_stack.pop() + body_text.strip())
    
    def end(self, name: str, parameters: Optional[List[Any]] = None) -> None:
        """
        处理元素结束事件
        
        Args:
            name: 元素名
            parameters: 参数数组，用于存储收集到的参数值
        """
        if self.body_text_stack and self.body_text_stack:
            # 获取完整的元素内容
            if self.body_text_stack:
                element_content = self.body_text_stack.pop()
                element_content += f"</{name}>"
                
                # 将内容设置到参数数组中
                if parameters is not None and self.param_index < len(parameters):
                    parameters[self.param_index] = element_content
    
    def clear(self) -> None:
        """清除状态"""
        self.body_text_stack.clear()
        self.current_element_name = ""
# 使用示例
if __name__ == "__main__":
    # 示例1: 使用MyCallParamRule的简化版本
    print("Example 1: Using MyCallParamRule")
    
    rule = MyCallParamRule(param_index=0)
    rule.set_attribute_name("id")
    
    # 模拟开始元素
    from xml.sax.xmlreader import AttributesImpl
    attrs = AttributesImpl({"id": "123", "name": "test"})
    rule.begin("element", attrs)
    
    # 模拟处理元素体
    rule.body("   Some text content   ")
    
    # 模拟结束元素
    parameters = [None]  # 参数数组
    rule.end("element", parameters)
    
    print(f"Collected parameter: {parameters[0]}")
    