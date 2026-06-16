import os
import bcrypt

# Load .env manually if it exists
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

PASSWORD_SALT = os.getenv("PASSWORD_SALT", "")
if not PASSWORD_SALT:
    raise RuntimeError("Security configuration error: PASSWORD_SALT environment variable is required and cannot be empty!")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt and an environment-defined salt."""
    salted_password = password + PASSWORD_SALT
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(salted_password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against its bcrypt hash (requiring env salt)."""
    try:
        salted_password = plain_password + PASSWORD_SALT
        return bcrypt.checkpw(salted_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def is_hashed(password: str) -> bool:
    """Check if a password string is already a bcrypt hash."""
    return len(password) == 60 and (password.startswith("$2b$") or password.startswith("$2a$") or password.startswith("$2y$"))
