import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "matches")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.models import Match, User  # noqa: F401
    from sqlalchemy import text

    # Create database if it does not exist
    temp_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    temp_engine = create_engine(temp_url)
    with temp_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"))
        conn.commit()
    temp_engine.dispose()

    Base.metadata.create_all(bind=engine)

    # Pre-populate default admin user and migrate existing passwords
    from app.security import hash_password, is_hashed
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            default_user = User(usergmail="admin@gmail.com", password=hash_password("admin123"))
            db.add(default_user)
            db.commit()
            print("Default admin user created: admin@gmail.com / admin123 (hashed)")
        else:
            # Check for any users with unhashed passwords and hash them
            users = db.query(User).all()
            updated_count = 0
            for u in users:
                if not is_hashed(u.password):
                    u.password = hash_password(u.password)
                    updated_count += 1
            if updated_count > 0:
                db.commit()
                print(f"Migrated {updated_count} user password(s) to hashed format.")
    except Exception as e:
        print(f"Error seeding/migrating user: {e}")
    finally:
        db.close()
