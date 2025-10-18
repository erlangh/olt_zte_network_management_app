"""
Database initialization script
Run this to create all tables and initial admin user
"""

from app.db.database import init_db, SessionLocal
from app.models.user import User
from app.core.security import get_password_hash


def create_admin_user():
    """Create default admin user if not exists"""
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            # Create admin user
            admin = User(
                username="admin",
                email="admin@localhost",
                full_name="System Administrator",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_superuser=True
            )
            db.add(admin)
            db.commit()
            print("✓ Admin user created successfully")
            print("  Username: admin")
            print("  Password: admin123")
            print("  IMPORTANT: Change this password after first login!")
        else:
            print("✓ Admin user already exists")
            
    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    print("-" * 50)
    
    # Create all tables
    print("Creating database tables...")
    init_db()
    print("✓ Database tables created")
    
    # Create admin user
    print("\nCreating admin user...")
    create_admin_user()
    
    print("-" * 50)
    print("Database initialization complete!")
