from app.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    conn.execute(text("ALTER TABLE matches ADD COLUMN is_selected BOOLEAN DEFAULT FALSE;"))
    conn.commit()
    print("Column added.")
