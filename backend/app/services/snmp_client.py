from pysnmp.hlapi import *
from typing import Optional, Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class SNMPClient:
    """SNMP Client for ZTE C320 OLT"""
    
    # ZTE C320 OIDs
    OID_SYSTEM_DESCR = "1.3.6.1.2.1.1.1.0"
    OID_SYSTEM_UPTIME = "1.3.6.1.2.1.1.3.0"
    OID_SYSTEM_NAME = "1.3.6.1.2.1.1.5.0"
    
    # ONU related OIDs (example - may need adjustment for ZTE C320)
    OID_ONU_STATUS = "1.3.6.1.4.1.3902.1012.3.28.1.1.3"  # ONU operational status
    OID_ONU_RX_POWER = "1.3.6.1.4.1.3902.1012.3.28.2.1.5"  # ONU RX power
    OID_ONU_TX_POWER = "1.3.6.1.4.1.3902.1012.3.28.2.1.6"  # ONU TX power
    OID_ONU_DISTANCE = "1.3.6.1.4.1.3902.1012.3.28.1.1.8"  # ONU distance
    OID_ONU_SN = "1.3.6.1.4.1.3902.1012.3.28.1.1.5"  # ONU Serial Number
    
    def __init__(self, host: str, community: str = "public", port: int = 161, version: str = "2c"):
        self.host = host
        self.community = community
        self.port = port
        self.version = version
        
    def _get_snmp_version(self):
        """Get SNMP version object"""
        if self.version == "1":
            return 0  # SNMPv1
        elif self.version == "2c":
            return 1  # SNMPv2c
        else:
            return 1  # Default to v2c
    
    def get(self, oid: str) -> Optional[str]:
        """
        Perform SNMP GET request
        
        Args:
            oid: SNMP OID to query
            
        Returns:
            Value as string or None if error
        """
        try:
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(self.community, mpModel=self._get_snmp_version()),
                UdpTransportTarget((self.host, self.port), timeout=5, retries=2),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )
            
            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
            
            if errorIndication:
                logger.error(f"SNMP error: {errorIndication}")
                return None
            elif errorStatus:
                logger.error(f"SNMP error: {errorStatus.prettyPrint()}")
                return None
            else:
                for varBind in varBinds:
                    return str(varBind[1])
                    
        except Exception as e:
            logger.error(f"SNMP GET error: {str(e)}")
            return None
    
    def walk(self, oid: str) -> List[Tuple[str, str]]:
        """
        Perform SNMP WALK request
        
        Args:
            oid: Base OID to walk
            
        Returns:
            List of (oid, value) tuples
        """
        results = []
        try:
            iterator = nextCmd(
                SnmpEngine(),
                CommunityData(self.community, mpModel=self._get_snmp_version()),
                UdpTransportTarget((self.host, self.port), timeout=5, retries=2),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                lexicographicMode=False
            )
            
            for errorIndication, errorStatus, errorIndex, varBinds in iterator:
                if errorIndication:
                    logger.error(f"SNMP walk error: {errorIndication}")
                    break
                elif errorStatus:
                    logger.error(f"SNMP walk error: {errorStatus.prettyPrint()}")
                    break
                else:
                    for varBind in varBinds:
                        oid_str = str(varBind[0])
                        value = str(varBind[1])
                        results.append((oid_str, value))
                        
        except Exception as e:
            logger.error(f"SNMP WALK error: {str(e)}")
            
        return results
    
    def test_connection(self) -> bool:
        """
        Test SNMP connection to device
        
        Returns:
            True if connection successful, False otherwise
        """
        result = self.get(self.OID_SYSTEM_DESCR)
        return result is not None
    
    def get_system_info(self) -> Dict[str, str]:
        """
        Get basic system information
        
        Returns:
            Dictionary with system info
        """
        return {
            "description": self.get(self.OID_SYSTEM_DESCR) or "Unknown",
            "uptime": self.get(self.OID_SYSTEM_UPTIME) or "0",
            "name": self.get(self.OID_SYSTEM_NAME) or "Unknown"
        }
    
    def get_onu_list(self, slot: int = None, port: int = None) -> List[Dict]:
        """
        Get list of ONUs from OLT
        
        Args:
            slot: Slot number (optional)
            port: Port number (optional)
            
        Returns:
            List of ONU dictionaries
        """
        onus = []
        
        # Walk ONU status OID
        status_results = self.walk(self.OID_ONU_STATUS)
        
        for oid, status in status_results:
            # Parse OID to extract slot/port/onu_id
            # OID format example: 1.3.6.1.4.1.3902.1012.3.28.1.1.3.{slot}.{port}.{onu_id}
            oid_parts = oid.split('.')
            if len(oid_parts) >= 3:
                try:
                    onu_slot = int(oid_parts[-3])
                    onu_port = int(oid_parts[-2])
                    onu_id = int(oid_parts[-1])
                    
                    # Filter by slot/port if specified
                    if slot is not None and onu_slot != slot:
                        continue
                    if port is not None and onu_port != port:
                        continue
                    
                    onu_info = {
                        "slot": onu_slot,
                        "port": onu_port,
                        "onu_id": onu_id,
                        "status": status,
                        "oid_suffix": f"{onu_slot}.{onu_port}.{onu_id}"
                    }
                    onus.append(onu_info)
                except (ValueError, IndexError):
                    continue
        
        return onus
    
    def get_onu_details(self, slot: int, port: int, onu_id: int) -> Dict:
        """
        Get detailed information for specific ONU
        
        Args:
            slot: Slot number
            port: Port number
            onu_id: ONU ID
            
        Returns:
            Dictionary with ONU details
        """
        suffix = f".{slot}.{port}.{onu_id}"
        
        details = {
            "slot": slot,
            "port": port,
            "onu_id": onu_id,
            "status": self.get(f"{self.OID_ONU_STATUS}{suffix}"),
            "rx_power": self.get(f"{self.OID_ONU_RX_POWER}{suffix}"),
            "tx_power": self.get(f"{self.OID_ONU_TX_POWER}{suffix}"),
            "distance": self.get(f"{self.OID_ONU_DISTANCE}{suffix}"),
            "sn": self.get(f"{self.OID_ONU_SN}{suffix}")
        }
        
        # Convert power values from raw to dBm if needed
        if details["rx_power"]:
            try:
                # ZTE often returns power in 0.01 dBm units
                details["rx_power"] = float(details["rx_power"]) / 100
            except:
                pass
                
        if details["tx_power"]:
            try:
                details["tx_power"] = float(details["tx_power"]) / 100
            except:
                pass
        
        return details
