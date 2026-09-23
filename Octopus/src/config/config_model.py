"""
Configuration model for parsing and managing configuration files.

This module provides functionality to parse XML configuration files,
manage configuration objects, and detect configuration changes.
"""

import os
import sys
import time
from typing import Optional, List, Dict, Any, ClassVar
from pathlib import Path
from dataclasses import dataclass, field
from threading import Lock

# Import existing configuration classes
from .tps_config_bean import TPsConfigBean
from .tp_config_bean import TPConfigBean
from .mq_config_bean import MqConfigBean
from .ftp_config_bean import FtpConfigBean
from .my_parser import MyParser



@dataclass
class FileInfo:
    """Information about a configuration file"""
    path: Path
    last_modified: float = 0.0
    exists: bool = False
    
    def update_last_modified(self) -> None:
        """Update the last modified timestamp"""
        if self.path.exists():
            self.last_modified = self.path.stat().st_mtime
            self.exists = True
        else:
            self.exists = False


class ConfigModel:
    """
    Configuration model for parsing and managing configuration files.
    
    This class handles loading, parsing, and managing configuration
    from XML files, with support for change detection and extension.
    """
    
    # Class variables (equivalent to Java static variables)
    tps_config: ClassVar[Optional[TPsConfigBean]] = None
    mq_configs: ClassVar[List[MqConfigBean]] = []
    ftp_configs: ClassVar[List[FtpConfigBean]] = []
    
    # File information
    config_file: ClassVar[Optional[FileInfo]] = None
    mq_file: ClassVar[Optional[FileInfo]] = None
    ftp_file: ClassVar[Optional[FileInfo]] = None
    
    # Custom configuration file name (can override defaults)
    custom_config_file_name: ClassVar[Optional[str]] = None
    
    # Thread safety
    _lock: ClassVar[Lock] = Lock()
    _initialized: ClassVar[bool] = False
    
    @classmethod
    def initialize(cls, 
                   config_file_name: Optional[str] = None,
                   mq_file_name: Optional[str] = None,
                   ftp_file_name: Optional[str] = None) -> None:
        """
        Initialize the configuration model.
        
        Args:
            config_file_name: Optional custom configuration file name
            mq_file_name: Optional custom MQ configuration file name
            ftp_file_name: Optional custom FTP configuration file name
        """
        with cls._lock:
            if not cls._initialized:
                # Set custom file names if provided
                if config_file_name:
                    cls.custom_config_file_name = config_file_name
                
                # Initialize file info objects
                cls._initialize_file_info(
                    config_file_name or "config.xml",
                    mq_file_name or "mq.xml",
                    ftp_file_name or "ftp.xml"
                )
                
                cls._initialized = True
    
    @classmethod
    def _initialize_file_info(cls, 
                              config_file_name: str,
                              mq_file_name: str,
                              ftp_file_name: str) -> None:
        """Initialize file information objects"""
        # Find configuration files
        config_path = cls._find_resource_file(config_file_name)
        mq_path = cls._find_resource_file(mq_file_name)
        ftp_path = cls._find_resource_file(ftp_file_name)
        
        cls.config_file = FileInfo(config_path)
        cls.mq_file = FileInfo(mq_path)
        cls.ftp_file = FileInfo(ftp_path)
        
        # Update timestamps
        cls.config_file.update_last_modified()
        cls.mq_file.update_last_modified()
        cls.ftp_file.update_last_modified()
    
    @staticmethod
    def _find_resource_file(file_name: str) -> Path:
        """
        Find a resource file, searching in multiple locations.
        
        Args:
            file_name: Name of the file to find
            
        Returns:
            Path to the file
            
        Raises:
            FileNotFoundError: If file cannot be found
        """
        # Search locations (in order of priority)
        search_paths = [
            # 1. Current working directory
            Path.cwd() / file_name,
            # 2. Directory containing this module
            Path(__file__).parent / file_name,
            # 3. Absolute path
            Path(file_name),
        ]
        
        for path in search_paths:
            if path.exists():
                return path
        
        raise FileNotFoundError(f"Cannot find configuration file: {file_name}")
    
    @classmethod
    def load_configuration(cls) -> bool:
        """
        Load and parse all configuration files.
        
        Returns:
            True if configuration was loaded successfully, False otherwise
        """
        with cls._lock:
            try:
                # Ensure initialization
                if not cls._initialized:
                    cls.initialize()
                
                # Load main configuration
                if not cls._load_tps_configuration():
                    return False
                
                # Load MQ configuration
                cls._load_mq_configuration()
                
                # Load FTP configuration
                cls._load_ftp_configuration()
                
                # Process extensions
                cls._process_extensions()
                
                # Update file timestamps
                cls._update_file_timestamps()
                
                return True
                
            except Exception as e:
                print(f"Error loading configuration: {e}", file=sys.stderr)
                return False
    
    @classmethod
    def _load_tps_configuration(cls) -> bool:
        """Load trading partners configuration"""
        try:
            if not cls.config_file.exists:
                print(f"Configuration file not found: {cls.config_file.path}", 
                      file=sys.stderr)
                return False
            
            # Create parser
            parser = MyParser()
            parser.prepare_parse()  # Prepare parsing rules for trading partners
            
            # Parse configuration file
            config = parser.parse_xml(cls.config_file.path)
            
            if config is None:
                print("Failed to parse configuration file", file=sys.stderr)
                return False
            
            cls.tps_config = config
            return True
            
        except Exception as e:
            print(f"Error parsing trading partners configuration: {e}", 
                  file=sys.stderr)
            return False
    
    @classmethod
    def _load_mq_configuration(cls) -> None:
        """Load MQ configuration"""
        try:
            if not cls.mq_file.exists:
                print(f"MQ configuration file not found: {cls.mq_file.path}", 
                      file=sys.stderr)
                return
            
            # Create parser for MQ
            parser = MyParser()
            parser.prepare_parse_mq()  # Prepare parsing rules for MQ
            
            # Parse MQ configuration file
            mq_list = parser.parse_xml(cls.mq_file.path)
            
            if mq_list is not None:
                if isinstance(mq_list, list):
                    cls.mq_configs = mq_list
                else:
                    # If parser returns a single object, wrap it in a list
                    cls.mq_configs = [mq_list]
                    
        except Exception as e:
            print(f"Error parsing MQ configuration: {e}", file=sys.stderr)
    
    @classmethod
    def _load_ftp_configuration(cls) -> None:
        """Load FTP configuration"""
        try:
            if not cls.ftp_file.exists:
                print(f"FTP configuration file not found: {cls.ftp_file.path}", 
                      file=sys.stderr)
                return
            
            # Create parser for FTP
            parser = MyParser()
            parser.prepare_parse_ftp()  # Prepare parsing rules for FTP
            
            # Parse FTP configuration file
            ftp_list = parser.parse_xml(cls.ftp_file.path)
            
            if ftp_list is not None:
                if isinstance(ftp_list, list):
                    cls.ftp_configs = ftp_list
                else:
                    # If parser returns a single object, wrap it in a list
                    cls.ftp_configs = [ftp_list]
                    
        except Exception as e:
            print(f"Error parsing FTP configuration: {e}", file=sys.stderr)
    
    @classmethod
    def _process_extensions(cls) -> None:
        """Process configuration extensions"""
        if cls.tps_config is None:
            return
        
        try:
            # Process MQ extensions
            search_list = []
            
            # Add MQ configurations from TPS config
            if hasattr(cls.tps_config, 'get_mqs'):
                mqs = cls.tps_config.get_mqs()
                if mqs:
                    search_list.extend(mqs)
                    
                    # Extend each MQ configuration
                    for mq in mqs:
                        if hasattr(mq, 'do_extend'):
                            mq.do_extend(search_list)
            
            # Process error message MQ configuration
            if hasattr(cls.tps_config, 'get_error_msg'):
                error_msg = cls.tps_config.get_error_msg()
                if (error_msg and hasattr(error_msg, 'get_mq_conf')):
                    mq_conf = error_msg.get_mq_conf()
                    if mq_conf and hasattr(mq_conf, 'do_extend'):
                        mq_conf.do_extend(search_list)
            
            # Process alive message MQ configuration
            if hasattr(cls.tps_config, 'get_alive_msg'):
                alive_msg = cls.tps_config.get_alive_msg()
                if (alive_msg and hasattr(alive_msg, 'get_mq_conf')):
                    mq_conf = alive_msg.get_mq_conf()
                    if mq_conf and hasattr(mq_conf, 'do_extend'):
                        mq_conf.do_extend(search_list)
            
            # Process trading partner extensions
            if hasattr(cls.tps_config, 'get_partners'):
                partners = cls.tps_config.get_partners()
                if partners:
                    for partner in partners:
                        if hasattr(partner, 'do_extend'):
                            partner.do_extend(search_list)
                            
        except Exception as e:
            print(f"Error processing configuration extensions: {e}", 
                  file=sys.stderr)
    
    @classmethod
    def _update_file_timestamps(cls) -> None:
        """Update file modification timestamps"""
        cls.config_file.update_last_modified()
        cls.mq_file.update_last_modified()
        cls.ftp_file.update_last_modified()
    
    @classmethod
    def has_configuration_changed(cls) -> bool:
        """
        Check if any configuration file has changed.
        
        Returns:
            True if any configuration file has been modified, False otherwise
        """
        try:
            # Update current file timestamps
            config_changed = cls._check_file_change(cls.config_file)
            mq_changed = cls._check_file_change(cls.mq_file)
            ftp_changed = cls._check_file_change(cls.ftp_file)
            
            # If any file changed, update timestamps
            if config_changed or mq_changed or ftp_changed:
                if config_changed:
                    cls.config_file.update_last_modified()
                if mq_changed:
                    cls.mq_file.update_last_modified()
                if ftp_changed:
                    cls.ftp_file.update_last_modified()
                return True
                
            return False
            
        except Exception as e:
            print(f"Error checking configuration changes: {e}", file=sys.stderr)
            return False
    
    @staticmethod
    def _check_file_change(file_info: FileInfo) -> bool:
        """
        Check if a file has been modified.
        
        Args:
            file_info: File information object
            
        Returns:
            True if file has been modified, False otherwise
        """
        if not file_info.exists:
            return False
        
        current_mtime = file_info.path.stat().st_mtime
        return abs(current_mtime - file_info.last_modified) > 0.001
    
    @classmethod
    def reload_if_changed(cls) -> bool:
        """
        Reload configuration if any file has changed.
        
        Returns:
            True if configuration was reloaded, False otherwise
        """
        if cls.has_configuration_changed():
            print("Configuration files have changed, reloading...")
            return cls.load_configuration()
        return False
    
    @classmethod
    def get_tps_config(cls) -> Optional[TPsConfigBean]:
        """Get the trading partners configuration"""
        return cls.tps_config
    
    @classmethod
    def get_mq_configs(cls) -> List[MqConfigBean]:
        """Get all MQ configurations"""
        return cls.mq_configs.copy()
    
    @classmethod
    def get_ftp_configs(cls) -> List[FtpConfigBean]:
        """Get all FTP configurations"""
        return cls.ftp_configs.copy()
    
    @classmethod
    def set_tps_config(cls, config: TPsConfigBean) -> None:
        """Set the trading partners configuration"""
        with cls._lock:
            cls.tps_config = config
    
    @classmethod
    def print_configuration_summary(cls) -> None:
        """Print a summary of the current configuration"""
        print("=" * 60)
        print("Configuration Summary")
        print("=" * 60)
        
        if cls.tps_config:
            print(f"TPS Configuration: {cls.tps_config.name}")
            if hasattr(cls.tps_config, 'partners'):
                print(f"  Partners: {len(cls.tps_config.partners)}")
            if hasattr(cls.tps_config, 'controllers'):
                print(f"  Controllers: {len(cls.tps_config.controllers)}")
        else:
            print("TPS Configuration: Not loaded")
        
        print(f"MQ Configurations: {len(cls.mq_configs)}")
        print(f"FTP Configurations: {len(cls.ftp_configs)}")
        
        print(f"Config File: {cls.config_file.path}")
        print(f"  Last Modified: {time.ctime(cls.config_file.last_modified)}")
        print(f"  Exists: {cls.config_file.exists}")
        
        print(f"MQ File: {cls.mq_file.path}")
        print(f"  Last Modified: {time.ctime(cls.mq_file.last_modified)}")
        print(f"  Exists: {cls.mq_file.exists}")
        
        print(f"FTP File: {cls.ftp_file.path}")
        print(f"  Last Modified: {time.ctime(cls.ftp_file.last_modified)}")
        print(f"  Exists: {cls.ftp_file.exists}")
        print("=" * 60)


# Example usage and testing
if __name__ == "__main__":
    print("Testing ConfigModel class")
    print("=" * 60)
    
    # Test 1: Using the class-based ConfigModel
    print("\n1. Testing class-based ConfigModel:")
    
    # Initialize with default files
    ConfigModel.initialize()
    
    # Load configuration
    if ConfigModel.load_configuration():
        print("Configuration loaded successfully")
        
        # Print summary
        ConfigModel.print_configuration_summary()
        
        # Get configuration objects
        tps_config = ConfigModel.get_tps_config()
        mq_configs = ConfigModel.get_mq_configs()
        ftp_configs = ConfigModel.get_ftp_configs()
        
        print(f"TPS Config: {tps_config.name if tps_config else 'None'}")
        print(f"MQ Configs: {len(mq_configs)}")
        print(f"FTP Configs: {len(ftp_configs)}")
        
        # Check for changes
        if ConfigModel.has_configuration_changed():
            print("Configuration has changed!")
        else:
            print("Configuration has not changed")
    else:
        print("Failed to load configuration")