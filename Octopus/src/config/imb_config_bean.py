# imb_config_bean.py

from typing import Optional


class IMBConfigBean:
    """
    Configuration bean for IMB parameters.
    """
    
    def __init__(self):
        """
        Initialize the IMBConfigBean with default values.
        """
        self.imb_m_eye_catch: Optional[str] = None
        self.imb_m_iopu_cty: Optional[str] = None
        self.imb_m_layout: Optional[str] = None
        self.imb_m_tp_id_from: Optional[str] = None
        self.imb_m_tp_id_to: Optional[str] = None

    def set_imb_m_eye_catch(self, s: str) -> None:
        """
        Set the IMB eye catch.
        
        Args:
            s (str): IMB eye catch value.
        """
        self.imb_m_eye_catch = s

    def get_imb_m_eye_catch(self) -> Optional[str]:
        """
        Get the IMB eye catch.
        
        Returns:
            str: IMB eye catch value.
        """
        return self.imb_m_eye_catch

    def set_imb_m_iopu_cty(self, s: str) -> None:
        """
        Set the IMB IOPU country.
        
        Args:
            s (str): IMB IOPU country value.
        """
        self.imb_m_iopu_cty = s

    def get_imb_m_iopu_cty(self) -> Optional[str]:
        """
        Get the IMB IOPU country.
        
        Returns:
            str: IMB IOPU country value.
        """
        return self.imb_m_iopu_cty

    def set_imb_m_layout(self, s: str) -> None:
        """
        Set the IMB layout.
        
        Args:
            s (str): IMB layout value.
        """
        self.imb_m_layout = s

    def get_imb_m_layout(self) -> Optional[str]:
        """
        Get the IMB layout.
        
        Returns:
            str: IMB layout value.
        """
        return self.imb_m_layout

    def set_imb_m_tp_id_from(self, s: str) -> None:
        """
        Set the IMB TP ID from.
        
        Args:
            s (str): IMB TP ID from value.
        """
        self.imb_m_tp_id_from = s

    def get_imb_m_tp_id_from(self) -> Optional[str]:
        """
        Get the IMB TP ID from.
        
        Returns:
            str: IMB TP ID from value.
        """
        return self.imb_m_tp_id_from

    def set_imb_m_tp_id_to(self, s: str) -> None:
        """
        Set the IMB TP ID to.
        
        Args:
            s (str): IMB TP ID to value.
        """
        self.imb_m_tp_id_to = s

    def get_imb_m_tp_id_to(self) -> Optional[str]:
        """
        Get the IMB TP ID to.
        
        Returns:
            str: IMB TP ID to value.
        """
        return self.imb_m_tp_id_to

    def to_xml_string(self) -> str:
        """
        Convert this object to XML string.
        
        Returns:
            str: XML representation of the object.
        """
        return ("<imb>\n" +
                f"\t<imbMEyeCatch>{self.imb_m_eye_catch}</imbMEyeCatch>\n" +
                f"\t<imbMIopuCty>{self.imb_m_iopu_cty}</imbMIopuCty>\n" +
                f"\t<imbMLayout>{self.imb_m_layout}</imbMLayout>\n" +
                f"\t<imbMTpId_From>{self.imb_m_tp_id_from}</imbMTpId_From>\n" +
                f"\t<imbMTpId_To>{self.imb_m_tp_id_to}</imbMTpId_To>\n" +
                "</imb>")

    def __str__(self) -> str:
        """
        Convert this object to string.
        
        Returns:
            str: String representation of the object.
        """
        return (f"imbMEyeCatch->{self.imb_m_eye_catch}\n" +
                f"imbMIopuCty->{self.imb_m_iopu_cty}\n" +
                f"imbMLayout->{self.imb_m_layout}\n" +
                f"imbMTpId_From->{self.imb_m_tp_id_from}\n" +
                f"imbMTpId_To->{self.imb_m_tp_id_to}")


if __name__ == "__main__":
    # 测试代码
    config = IMBConfigBean()
    config.imb_m_iopu_cty="WWD"
    config.imb_m_layout="WWID1"
    config._imb_m_tp_id_from="GEOFLO"
    config._imb_m_tp_id_to="ISCIW"
    print(config)