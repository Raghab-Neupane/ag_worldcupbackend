import os
import sys
import getpass

# Add current directory to python path to import app modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Load environment variables from .env manually if not already loaded
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

from app.database import SessionLocal
from app.models import User
from app.security import hash_password

def main():
    print("=== Terminal User Creation Utility ===")
    
    # Prompt for credentials
    email = input("Enter user email: ").strip().lower()
    if not email or "@" not in email:
        print("Error: Invalid email format.")
        sys.exit(1)
        
    password = getpass.getpass("Enter password: ")
    if len(password) < 4:
        print("Error: Password must be at least 4 characters long.")
        sys.exit(1)
        
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        print("Error: Passwords do not match.")
        sys.exit(1)
        
    # Open database session
    db = SessionLocal()
    try:
        # Check if user already exists
        existing = db.query(User).filter(User.usergmail == email).first()
        if existing:
            print(f"Error: A user with email '{email}' already exists.")
            sys.exit(1)
            
        # Create user
        new_user = User(
            usergmail=email,
            password=hash_password(password)
        )
        db.add(new_user)
        db.commit()
        print(f"Success: User '{email}' created successfully with hashed password!")
    except Exception as e:
        db.rollback()
        print(f"Database error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
