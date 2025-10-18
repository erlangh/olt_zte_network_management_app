"""
Create sample data for testing
"""

from app.db.database import SessionLocal
from app.models.user import User
from app.models.olt import OLT, Slot, Port
from app.models.onu import ONU
from app.models.odp import ODP
from app.core.security import get_password_hash

def create_sample_data():
    db = SessionLocal()
    
    try:
        print("Creating sample data...")
        print("-" * 60)
        
        # Create admin user if not exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@localhost",
                full_name="System Administrator",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_superuser=True
            )
            db.add(admin)
            print("✓ Created admin user")
        else:
            print("✓ Admin user already exists")
        
        # Create sample OLT
        olt = db.query(OLT).filter(OLT.name == "OLT-Sample-01").first()
        if not olt:
            olt = OLT(
                name="OLT-Sample-01",
                ip_address="192.168.1.100",
                description="Sample OLT for testing",
                snmp_community="public",
                snmp_version="2c",
                snmp_port=161,
                telnet_enabled=True,
                telnet_port=23,
                vendor="ZTE",
                model="C320",
                location="Data Center A",
                latitude=-6.2088,
                longitude=106.8456,
                status="unknown"
            )
            db.add(olt)
            db.flush()  # Get the ID
            print(f"✓ Created sample OLT: {olt.name}")
            
            # Create sample slot
            slot = Slot(
                olt_id=olt.id,
                slot_number=1,
                card_type="GPON",
                status="online",
                description="GPON card slot 1"
            )
            db.add(slot)
            db.flush()
            
            # Create sample ports
            for i in range(1, 5):
                port = Port(
                    slot_id=slot.id,
                    port_number=i,
                    status="up",
                    description=f"PON port {i}",
                    total_onus=0,
                    online_onus=0,
                    offline_onus=0
                )
                db.add(port)
            
            print(f"✓ Created slot and 4 ports for OLT")
        else:
            print("✓ Sample OLT already exists")
        
        # Create sample ODPs
        odp_data = [
            {
                "name": "ODP-001",
                "code": "ODP001",
                "address": "Jl. Sudirman No. 123",
                "splitter_ratio": "1:8",
                "total_ports": 8,
                "latitude": -6.2088,
                "longitude": 106.8456
            },
            {
                "name": "ODP-002",
                "code": "ODP002",
                "address": "Jl. Thamrin No. 456",
                "splitter_ratio": "1:16",
                "total_ports": 16,
                "latitude": -6.1951,
                "longitude": 106.8230
            }
        ]
        
        for odp_info in odp_data:
            existing = db.query(ODP).filter(ODP.name == odp_info["name"]).first()
            if not existing:
                odp = ODP(**odp_info, available_ports=odp_info["total_ports"])
                db.add(odp)
                print(f"✓ Created sample ODP: {odp_info['name']}")
            else:
                print(f"✓ Sample ODP {odp_info['name']} already exists")
        
        # Create sample ONUs
        onu_data = [
            {
                "sn": "ZTEG12345678",
                "customer_name": "John Doe",
                "customer_phone": "081234567890",
                "customer_address": "Jl. Kebon Jeruk No. 1",
                "service_plan": "100 Mbps",
                "status": "online"
            },
            {
                "sn": "ZTEG87654321",
                "customer_name": "Jane Smith",
                "customer_phone": "081234567891",
                "customer_address": "Jl. Kebon Jeruk No. 2",
                "service_plan": "50 Mbps",
                "status": "offline"
            }
        ]
        
        # Get first port for ONUs
        port = db.query(Port).first()
        if port:
            for onu_info in onu_data:
                existing = db.query(ONU).filter(ONU.sn == onu_info["sn"]).first()
                if not existing:
                    onu = ONU(
                        **onu_info,
                        olt_id=olt.id if olt else 1,
                        port_id=port.id,
                        mac_address="00:11:22:33:44:55",
                        onu_id=1,
                        rx_power=-25.5,
                        tx_power=2.3,
                        distance=1500,
                        vendor="ZTE",
                        model="F660"
                    )
                    db.add(onu)
                    print(f"✓ Created sample ONU: {onu_info['sn']}")
                else:
                    print(f"✓ Sample ONU {onu_info['sn']} already exists")
        
        db.commit()
        print("-" * 60)
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
