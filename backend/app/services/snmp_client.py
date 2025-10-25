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

    def get(self, oid: str) -> Optional[str]:
        try:
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(self.community, mpModel=1),
                UdpTransportTarget((self.host, self.port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )
            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
            if errorIndication or errorStatus:
                return None
            for name, val in varBinds:
                return str(val)
        except Exception:
            return None
        return None

    def walk(self, oid: str) -> List[Tuple[str, str]]:
        results: List[Tuple[str, str]] = []
        try:
            for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
                SnmpEngine(),
                CommunityData(self.community, mpModel=1),
                UdpTransportTarget((self.host, self.port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                lexicographicMode=False
            ):
                if errorIndication or errorStatus:
                    break
                for name, val in varBinds:
                    results.append((str(name), str(val)))
        except Exception:
            pass
        return results

    def test_connection(self) -> bool:
        return self.get(self.OID_SYSTEM_DESCR) is not None

    def get_system_info(self) -> Dict:
        return {
            "description": self.get(self.OID_SYSTEM_DESCR),
            "uptime": self.get(self.OID_SYSTEM_UPTIME),
            "name": self.get(self.OID_SYSTEM_NAME)
        }

    @staticmethod
    def decode_port_index(port_index: int) -> int:
        """
        ZTE encodes port identifier in a 32-bit index.
        Empirically, the PON port number sits in the high-word low byte.
        Extract with (index >> 16) & 0xFF to get human port number.
        """
        try:
            return (int(port_index) >> 16) & 0xFF
        except Exception:
            return int(port_index)

    def get_onu_list(self, slot: int = None, port: int = None) -> List[Dict]:
        """
        Get list of ONUs from OLT
        Returns list with both decoded port and raw suffix for detail queries.
        """
        onus: List[Dict] = []
        status_results = self.walk(self.OID_ONU_STATUS)
        for oid, status in status_results:
            oid_parts = oid.split('.')
            if len(oid_parts) >= 3:
                try:
                    onu_slot = int(oid_parts[-3])
                    port_idx = int(oid_parts[-2])
                    onu_id = int(oid_parts[-1])

                    decoded_port = self.decode_port_index(port_idx)

                    if slot is not None and onu_slot != slot:
                        continue
                    if port is not None and decoded_port != port:
                        continue

                    suffix_raw = f"{onu_slot}.{port_idx}.{onu_id}"
                    onu_info = {
                        "slot": onu_slot,
                        "port": decoded_port,
                        "onu_id": onu_id,
                        "status": status,
                        "oid_suffix": suffix_raw,
                        "port_index": port_idx
                    }
                    onus.append(onu_info)
                except (ValueError, IndexError):
                    continue
        return onus

    def get_onu_details_suffix(self, suffix_raw: str) -> Dict:
        """Fetch ONU details using the raw OID suffix returned by walk."""
        details = {
            "status": self.get(f"{self.OID_ONU_STATUS}.{suffix_raw}"),
            "rx_power": self.get(f"{self.OID_ONU_RX_POWER}.{suffix_raw}"),
            "tx_power": self.get(f"{self.OID_ONU_TX_POWER}.{suffix_raw}"),
            "distance": self.get(f"{self.OID_ONU_DISTANCE}.{suffix_raw}"),
            "sn": self.get(f"{self.OID_ONU_SN}.{suffix_raw}")
        }
        # Convert power values
        try:
            if details["rx_power"] is not None:
                details["rx_power"] = float(details["rx_power"]) / 100
        except Exception:
            pass
        try:
            if details["tx_power"] is not None:
                details["tx_power"] = float(details["tx_power"]) / 100
        except Exception:
            pass
        return details

    def get_onu_details(self, slot: int, port: int, onu_id: int) -> Dict:
        """
        Legacy helper: build suffix using decoded port number.
        Note: On some ZTE MIBs this may not resolve; prefer get_onu_details_suffix.
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
        try:
            if details["rx_power"] is not None:
                details["rx_power"] = float(details["rx_power"]) / 100
        except Exception:
            pass
        try:
            if details["tx_power"] is not None:
                details["tx_power"] = float(details["tx_power"]) / 100
        except Exception:
            pass
        return details
