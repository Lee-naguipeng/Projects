# private_config.py

import xml.sax
import xml.sax.handler
from typing import Dict, List, Optional, Any
from pathlib import Path


class PrivateConfig(xml.sax.handler.ContentHandler):
    """
    Parse and store private configuration from XML files.
    
    This class reads an XML configuration file and stores key-value pairs
    where keys are constructed from the XML element hierarchy.
    """

    def __init__(self, file_path: Path):
        """
        Initialize the PrivateConfig with a file path.
        
        Args:
            file_path (Path): Path to the XML configuration file.
        """
        super().__init__()
        self._file_path = file_path
        self._nodes: List[str] = []
        self._values: Dict[str, str] = {}

    def get_value(self, key: str) -> Optional[str]:
        """
        Get a value by its key.
        
        Args:
            key (str): The key to look up.
            
        Returns:
            str: The value associated with the key, or None if not found.
        """
        return self._values.get(key)

    def set_value(self, key: str, value: str) -> None:
        """
        Set a key-value pair.
        
        Args:
            key (str): The key.
            value (str): The value.
        """
        self._values[key] = value

    def parse(self) -> None:
        """
        Parse the XML file and populate the configuration values.
        
        This method reads the XML file and builds a dictionary of key-value pairs
        where keys represent the path to each element in the XML hierarchy.
        """
        try:
            parser = xml.sax.make_parser()
            parser.setContentHandler(self)
            parser.parse(str(self._file_path))
        except xml.sax.SAXParseException as e:
            print(f"Parse error at line {e.getLineNumber()}: {e}")
        except Exception as e:
            print(f"Error parsing configuration: {e}")

    def startElement(self, name: str, attrs: Any) -> None:
        """
        Handle the start of an XML element.
        
        Args:
            name (str): The element name.
            attrs (Any): The element attributes.
        """
        self._nodes.append(name)

    def endElement(self, name: str) -> None:
        """
        Handle the end of an XML element.
        
        Args:
            name (str): The element name.
        """
        if self._nodes:
            self._nodes.pop()

    def characters(self, content: str) -> None:
        """
        Handle character data within an XML element.
        
        Args:
            content (str): The character data.
        """
        # Clean up the value using translate method for better performance
        value = content.translate(str.maketrans('', '', '\t\n '))
        if not value:
            return
        
        # Build the key from node hierarchy
        if self._nodes:
            key = "->".join(self._nodes)
            self._values[key] = value

    def __str__(self) -> str:
        """
        Return a string representation of all configuration elements.
        
        Returns:
            str: Formatted string with all key-value pairs.
        """
        lines = []
        for key, val in sorted(self._values.items()):
            lines.append(f"{key} : {val}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        """
        Return a detailed representation for debugging.
        
        Returns:
            str: Detailed string representation.
        """
        return f"PrivateConfig(file_path={self._file_path!r}, values_count={len(self._values)})"


def load_private_config(file_path: str) -> PrivateConfig:
    """
    Load and parse a private configuration file.
    
    Args:
        file_path (str): Path to the XML configuration file.
        
    Returns:
        PrivateConfig: Parsed configuration object.
    """
    config = PrivateConfig(Path(file_path))
    config.parse()
    return config


if __name__ == "__main__":
    config = PrivateConfig(Path("tpdConfig.xml"))
    config.parse()
    print(config)