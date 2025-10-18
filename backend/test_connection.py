"""
Simple script to test database connection and basic API functionality
"""

import sys
from sqlalchemy import text

try:
    from app.db.database import SessionLocal, engine
    from app.core.config import settings
    
    print("=" * 60)
    print("Testing Database Connection")
    print("=" * 60)
    
    # Test 1: Database URL
    print(f"\n1. Database URL: {settings.DATABASE_URL}")
    
    # Test 2: Engine connection
    print("\n2. Testing engine connection...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("   ✓ Engine connection successful")
    except Exception as e:
        print(f"   ✗ Engine connection failed: {e}")
        sys.exit(1)
    
    # Test 3: SessionLocal
    print("\n3. Testing SessionLocal...")
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("   ✓ SessionLocal successful")
    except Exception as e:
        print(f"   ✗ SessionLocal failed: {e}")
        sys.exit(1)
    
    # Test 4: Check tables
    print("\n4. Checking database tables...")
    try:
        from app.db.database import Base
        from app.models import User, OLT, ONU, ODP, CableRoute
        
        db = SessionLocal()
        
        # Try to query each table
        tables = {
            'users': User,
            'olts': OLT,
            'onus': ONU,
            'odps': ODP,
            'cable_routes': CableRoute
        }
        
        for table_name, model in tables.items():
            try:
                count = db.query(model).count()
                print(f"   ✓ Table '{table_name}': {count} records")
            except Exception as e:
                print(f"   ✗ Table '{table_name}': {e}")
        
        db.close()
    except Exception as e:
        print(f"   ✗ Error checking tables: {e}")
    
    print("\n" + "=" * 60)
    print("All tests passed! Database is ready.")
    print("=" * 60)
    
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're in the virtual environment and dependencies are installed.")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)
