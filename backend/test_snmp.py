"""
Test SNMP connection to OLT
Usage: python test_snmp.py <olt_ip> [community]
"""

import sys
from app.services.snmp_client import SNMPClient

def test_snmp_connection(host, community="public"):
    print("=" * 60)
    print(f"Testing SNMP Connection to {host}")
    print("=" * 60)
    
    # Create SNMP client
    snmp = SNMPClient(host=host, community=community)
    
    # Test 1: Connection test
    print("\n1. Testing connection...")
    is_connected = snmp.test_connection()
    if is_connected:
        print("   ✓ Connection successful")
    else:
        print("   ✗ Connection failed")
        print("\nTroubleshooting:")
        print("  - Check if OLT is reachable: ping", host)
        print("  - Verify SNMP is enabled on OLT")
        print("  - Check SNMP community string")
        print("  - Verify firewall allows SNMP (UDP 161)")
        return
    
    # Test 2: Get system info
    print("\n2. Getting system information...")
    try:
        sys_info = snmp.get_system_info()
        print(f"   System Description: {sys_info.get('description', 'N/A')}")
        print(f"   System Uptime: {sys_info.get('uptime', 'N/A')}")
        print(f"   System Name: {sys_info.get('name', 'N/A')}")
    except Exception as e:
        print(f"   ✗ Error getting system info: {e}")
    
    # Test 3: Try to get ONU list
    print("\n3. Attempting to discover ONUs...")
    try:
        onus = snmp.get_onu_list()
        if onus:
            print(f"   ✓ Discovered {len(onus)} ONUs")
            for onu in onus[:5]:  # Show first 5
                print(f"     - Slot {onu['slot']}, Port {onu['port']}, ONU ID {onu['onu_id']}")
            if len(onus) > 5:
                print(f"     ... and {len(onus) - 5} more")
        else:
            print("   ℹ No ONUs discovered")
            print("   Note: ONU OIDs may need adjustment for your ZTE C320 firmware")
    except Exception as e:
        print(f"   ✗ Error discovering ONUs: {e}")
    
    print("\n" + "=" * 60)
    print("SNMP test completed")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_snmp.py <olt_ip> [community]")
        print("Example: python test_snmp.py 192.168.1.100 public")
        sys.exit(1)
    
    host = sys.argv[1]
    community = sys.argv[2] if len(sys.argv) > 2 else "public"
    
    test_snmp_connection(host, community)
