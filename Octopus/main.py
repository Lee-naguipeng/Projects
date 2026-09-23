import sys
import os
import runpy

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

result = runpy.run_module('src.config.interface_config_bean', run_name="__main__")




