# error_constant.py

"""
Error constants used throughout the application.

The first character 'I' stands for Ivy's code.

The second character indicates the class:
- 'I' stands for Interface class
- 'Q' stands for MQHelper class
- 'F' stands for FileHelper class
- 'R' stands for Replace class
- 'T' stands for Trim class

If the second character is 'I', then the third number indicates:
- 0 stands for TransferImp
- 1 stands for File2MQ
- 2 stands for MQ2File
- 3 stands for EDIMQ2File
- 4 stands for IMBMQ2File
- 5 stands for MultiEDIMQ2File
- 6 stands for MultiIMBMQ2File
- 7 stands for SingleEDIMQ2File
- 8 stands for SingleIMBMQ2File
- 9 stands for File2Ftp

If the second character is 'Q', then the third number indicates:
- 1 stands for put error occurred
- 2 stands for get error occurred
- 3 stands for other error occurred

If the second character is 'F', then the third number indicates:
- 1 stands for FileHelper class
- 2 stands for CommonFile class
- 3 stands for AnsiX12 class
- 4 stands for ImbFormat class
- 5 stands for XmlFormat class

The last three characters stand for the error number under the former three character's error condition.
"""

from typing import Final


class ErrorConstant:
    """
    Error constants used throughout the application.
    """
    
    # Handle MQ transaction in TransferImp.mqCommitChanges() method
    II0001: Final[str] = "II0001"
    
    # The filter subclass that got from config file was not a subclass of FilterImp
    II1001: Final[str] = "II1001"
    
    # ERROR: File2MQ.transfer() failed! File size is larger than limited size
    II1002: Final[str] = "II1002"
    
    # ERROR: File2MQ.transfer() failed!
    II1003: Final[str] = "II1003"
    
    # ERROR: Exception occurred when File2MQ.processFile2MQ() executed: Failed to put data to queue
    II1004: Final[str] = "II1004"
    
    # ERROR: File2MQ.processFile2MQ() occurred error: Data could not be archived successfully
    II1005: Final[str] = "II1005"
    
    # ERROR: There is no 'dir' element in 'file' segment
    II1006: Final[str] = "II1006"
    
    # ERROR: There is no 'archiveDir' element in 'file' segment
    II1007: Final[str] = "II1007"
    
    # ERROR: File2MQ.processFile2MQ() can only a process a file or directory, wrong archive directory was passed!
    II1008: Final[str] = "II1008"
    
    # Exception Error in MQ2File.transfer() method. The bundle keys and bundle values could not
    # be read successfully from the config file
    II2001: Final[str] = "II2001"
    
    # Exception Error in MQ2File.transfer() method. The messages could not be read from queue successfully
    II2002: Final[str] = "II2002"
    
    # RC=340X Fatal MQException occurred in MQ2File.readMsgUnderCursor() method while trying
    # to get message under cursor
    II2003: Final[str] = "II2003"
    
    # Fatal Error: Exception occurred in MQ2File.setBundleValue() method
    II2004: Final[str] = "II2004"
    
    # Exception Error in MQ2File.write2Dir() method.
    # The data could not write to destination directory successfully
    II2005: Final[str] = "II2005"
    
    # Exception Error in MQ2File.write2Dir() method.
    # The data could not write to archive directory successfully
    II2006: Final[str] = "II2006"
    
    # Exception Error in MQ2File.write2Dir() method.
    # The specified destination dir does not exist
    II2007: Final[str] = "II2007"
    
    # Exception Error in MQ2File.write2Dir() method.
    # The specified destination dir is not a dir
    II2008: Final[str] = "II2008"
    
    # Exception Error in MQ2File.write2ArchiveDir() method.
    # The archiveDir element isn't configured in config file
    II2011: Final[str] = "II2011"
    
    # ERROR: RC=340X Fatal MQException occurred in EDIMQ2File.readBundle() method while browsed from queue
    II3001: Final[str] = "II3001"
    
    # ERROR: Couldn't find BundleValue in the config file while processing EDIMQ2File.readBundle() method
    II3002: Final[str] = "II3002"
    
    # Different count of bundle messages were processed compare to the bundle size value in config file
    # while EDIMQ2File.readBundle() method was processing edi data message
    II3003: Final[str] = "II3003"
    
    # ERROR: Fatal Exception occurred in EDIMQ2File.readBundle() method
    II3004: Final[str] = "II3004"
    
    # Fatal MQexception occurred in EDIMQ2File.calcBundleSize() while BROWSing message from queue
    II3005: Final[str] = "II3005"
    
    # Fatal Exception occurred in EDIMQ2File.calcBundleSize() method
    II3006: Final[str] = "II3006"
    
    # Fatal InterruptedException in EDIMQ2File.getBundledSize() method while processing Thread.sleep
    II3007: Final[str] = "II3007"
    
    # Fatal Error occurred while executed EDIMQ2File.getBundledSize() method
    II3008: Final[str] = "II3008"
    
    # ERROR: RC=3406 Fatal MQexception occurred in IMBMQ2File.readBundle() method while browsing message from queue
    II4001: Final[str] = "II4001"
    
    # ERROR: Couldn't find BundleValue in the config file while processing IMBMQ2File.readBundle() method
    II4002: Final[str] = "II4002"
    
    # Fatal MQError in IMBMQ2File.readBundle() method while processing imb data message
    II4003: Final[str] = "II4003"
    
    # Fatal Error in IMBMQ2File.readBundle() method while processing imb data message
    II4004: Final[str] = "II4004"
    
    # RC=3406 Fatal MQexception occurred in IMBMQ2File.calcBundleSize() method,
    # while this method was BROWSing message from queue
    II4005: Final[str] = "II4005"
    
    # ERROR: Fatal MQException occurred in IMBMQ2File.calcBundleSize() method
    II4006: Final[str] = "II4006"
    
    # RC=340X Fatal InterruptedException occurred in IMBMQ2File.getBundledSize() method
    # while processing Thread.sleep
    II4007: Final[str] = "II4007"
    
    # Fatal Error occurred in IMBMQ2File.getBundledSize() method
    II4008: Final[str] = "II4008"
    
    # Fatal IO Error in IMBMQ2File.getBundledSize() method
    II4009: Final[str] = "II4009"
    
    # Fatal MQException Error in IMBMQ2File.getBundledSize() method
    II4010: Final[str] = "II4010"
    
    # Fatal Error occurred:  NullPointerException in IMBMQ2File.getBundledSize() while this method
    # was running
    II4011: Final[str] = "II4011"
    
    # Fatal IOError occurred while executed IMBMQ2File.readBundle() method
    # was running
    II4012: Final[str] = "II4012"
    
    # Fatal MQError occurred while executed IMBMQ2File.readBundle() method
    # was running
    II4013: Final[str] = "II4013"
    
    # Fatal MQError occurred while executed IMBMQ2File.calcBundleSize() method
    # was running
    II4014: Final[str] = "II4014"
    
    # Fatal IOError occurred while executed IMBMQ2File.calcBundleSize() method
    # was running
    II4015: Final[str] = "II4015"
    
    # Fatal IOError occurred while executed IMBMQ2File.calcBundleSize() method
    # was running
    II4016: Final[str] = "II4016"
    
    # Fatal IOError occurred while executed IMBMQ2File.readBundle() method
    # was running
    II4017: Final[str] = "II4017"
    
    # Config file is wrong. The configured file type isn't EDI!
    II5001: Final[str] = "II5001"
    
    # Config Error occurred in MultiEDIMQ2File.processMultiEDIMQ2Files() method while processing messages
    # The filter class in the config file isn't a subclass of FilterImp
    II5002: Final[str] = "II5002"
    
    # MQ error occurred while executed MultiEDIMQ2File.processMultiEDIMQ2Files() method
    II5003: Final[str] = "II5003"
    
    # Error occurred in MultiEDIMQ2File.processMultiEDIMQ2Files() method while processing messages
    II5004: Final[str] = "II5004"
    
    # Config file is wrong. The configured file type isn't imb!
    II6001: Final[str] = "II6001"
    
    # Config Error occurred in MultiIMBMQ2File.processMultiIMBMQ2Files() method while processing messages
    # The filter class in the config file isn't a subclass of FilterImp
    II6002: Final[str] = "II6002"
    
    # MQ error occurred while executed MultiIMBMQ2File.processMultiIMBMQ2Files() method
    II6003: Final[str] = "II6003"
    
    # Error occurred while executed MultiIMBMQ2File.processMultiIMBMQ2Files() method
    II6004: Final[str] = "II6004"
    
    # Config Error occurred in SingleEDIMQ2File.processSingleEDIMQ2Files() method
    # The configured file type isn't edi!
    II7001: Final[str] = "II7001"
    
    # Config Error occurred in SingleEDIMQ2File.processSingleEDIMQ2Files() method while processing messages
    # The filter class in the config file isn't a subclass of FilterImp
    II7002: Final[str] = "II7002"
    
    # MQ Error occurred while executed SingleIMBMQ2File.processSingleIMBMQ2Files() method
    II7003: Final[str] = "II7003"
    
    # Error occurred while executed SingleIMBMQ2File.processSingleIMBMQ2Files() method
    II7004: Final[str] = "II7004"
    
    # Config Error occurred in SingleIMBMQ2File.processSingleIMBMQ2Files() method
    # The configured file type isn't imb!
    II8001: Final[str] = "II8001"
    
    # Config Error occurred in SingleIMBMQ2File.processSingleIMBMQ2Files() method while processing messages
    # The filter class in the config file isn't a subclass of FilterImp
    II8002: Final[str] = "II8002"
    
    # MQ Error occurred while executed SingleIMBMQ2File.processSingleIMBMQ2Files() method
    II8003: Final[str] = "II8003"
    
    # Error occurred while executed SingleIMBMQ2File.processSingleIMBMQ2Files() method
    II8004: Final[str] = "II8004"
    
    # File2Ftp.transfer() can only a process a file or directory, wrong directory was passed
    II9001: Final[str] = "II9001"
    
    # ERROR: File2Ftp.transfer() failed! File size is less than limited size,
    # Pls double check the configuration file and make sure the file size larger than the limited size!
    II9002: Final[str] = "II9002"
    
    # ERROR: File2Ftp.transfer() failed!
    II9003: Final[str] = "II9003"
    
    # ERROR: There is no 'dir' element in 'file' segment
    II9004: Final[str] = "II9004"
    
    # ERROR: There is no 'archiveDir' element in 'file' segment
    II9005: Final[str] = "II9005"
    
    # ERROR: File2Ftp.processFile2Ftp() can only a process a file or directory, wrong archive directory was passed!
    II9006: Final[str] = "II9006"
    
    # ERROR: File2MQ.processFile2MQ() : File could not be read
    II9007: Final[str] = "II9007"
    
    # Private filter info config error occurred while Replace.filtrate() method
    # occurred, the private config shouldn't be null
    IR1001: Final[str] = "IR1001"
    
    # Private filter info config error occurred while Replace.filtrate() method
    # occurred, the origin character in the private config shouldn't be null!
    IR1002: Final[str] = "IR1002"
    
    # Fatal error occurred in Replace.filtrate() method
    IR1003: Final[str] = "IR1003"
    
    # ERROR: Fatal error occurred in Replace.filtrate() method. Replace.filtrate() failed!
    # The private config xml file doesn't exist!
    IR1004: Final[str] = "IR1004"
    
    # ERROR: Fatal error occurred in Trim.filtrate() method
    IT1001: Final[str] = "IT1001"
    
    # Error occurred while getmq configuration information from config file in MQHelper constructor method
    IQ3001: Final[str] = "IQ3001"
    
    # An IOException error occurs while the FileHelper.setFilePermission() method was running
    # Failed to set permission for the file
    IF1001: Final[str] = "IF1001"
    
    # An InterruptedException error occurs while the FileHelper.setFilePermission() method was running
    # Failed to set permission for the file
    IF1002: Final[str] = "IF1002"
    
    # An IOException error occurs while the CommonFile.setFileNameValues() method was running
    # Failed to set the file name
    IF2001: Final[str] = "IF2001"
    
    # An IOException error occurs while the CommonFile.fileCreateName() method was running
    # Failed to create the file name
    IF2002: Final[str] = "IF2002"
    
    # An NullPointerException error occurs while the AnsiX12.initInterchangeHeader() method was running
    # Failed to initial interchange header
    IF3001: Final[str] = "IF3001"
    
    # An NullPointerException error occurs while the AnsiX12.processAnsiX12() method was running
    # Failed to determine if the data is a UN/Edifact While processInterchangeHeader
    IF3002: Final[str] = "IF3002"
    
    # An NullPointerException error occurs while the AnsiX12.processAnsiX12() method was running
    # Failed to determine if the data is a UN/Edifact While processing rest of data
    IF3003: Final[str] = "IF3003"
    
    # An Exception error occurs while the AnsiX12.processInterchangeHeader() method was running
    # Failed to While processInterchangeHeader
    IF3004: Final[str] = "IF3004"
    
    # An Exception error occurs while the AnsiX12.processTransactionSetHdr() method was running
    # Failed to While processTransactionSetHdr
    IF3005: Final[str] = "IF3005"
    
    # An Exception error occurs while the ImbFormat's constructor method was created
    # Failed to create ImbFormat instance
    IF4001: Final[str] = "IF4001"
    
    # An Exception error occurs while the ImbFormat.processImbFormat() method was running
    # Failed to While processImbFormat
    IF4002: Final[str] = "IF4002"
    
    # An Exception error occurs while the ImbFormat.processMRcd() method was running
    # Failed to While processMRcd
    IF4003: Final[str] = "IF4003"
    
    # An Exception error occurs while the XmlFormat.formatPrettyXmlFile() method was running
    # Failed to While processing XML file in reformatPrettyXml
    IF5001: Final[str] = "IF5001"
    
    # An JDOMException error occurs while the XmlFormat.formatPrettyXmlFile() method was running
    # Failed to While Reading XML file in reformatPrettyXml
    IF5002: Final[str] = "IF5002"
    
    # An IOException error occurs while the XmlFormat.formatPrettyXmlFile() method was running
    # Failed to While Writing out XML file from reformatPrettyXml
    IF5003: Final[str] = "IF5003"
    
    # An JDOMException error occurs while the XmlFormat.processXmlFile() method was running
    # Failed to While processing XML file in processXmlFile
    IF5004: Final[str] = "IF5004"
    
    # An IOException error occurs while the XmlFormat.processXmlFile() method was running
    # Failed to While processing XML file in processXmlFile
    IF5005: Final[str] = "IF5005"