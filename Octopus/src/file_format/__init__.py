# __init__.py
"""
File Format Package Initialization Module

This module initializes the file_format package and provides convenient imports
for the file format processing classes used throughout the application.
"""

# Import file format classes
from .imb_inbound import IMBDRecord, IMBInbound

__all__ = [
    # File format classes
    'IMBDRecord',
    'IMBInbound'
]