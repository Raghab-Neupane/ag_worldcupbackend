import os
import bcrypt

PASSWORD_SALT = os.getenv("PASSWORD_SALT", "")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt and an environment-defined salt."""
    salted_password = password + PASSWORD_SALT
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(salted_password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against its bcrypt hash, with a fallback to verification without salt."""
    # 1. Try to verify with env salt
    try:
        salted_password = plain_password + PASSWORD_SALT
        if bcrypt.checkpw(salted_password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
    except Exception:
        pass

    # 2. Fallback to check without env salt (legacy support)
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def is_hashed(password: str) -> bool:
    """Check if a password string is already a bcrypt hash."""
    return len(password) == 60 and (password.startswith("$2b$") or password.startswith("$2a$") or password.startswith("$2y$"))
