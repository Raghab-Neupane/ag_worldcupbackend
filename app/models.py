from sqlalchemy import Column, DateTime, Integer, String, Boolean, func, JSON
from app.database import Base



class Match(Base):
    __tablename__ = "matches"

    match_no = Column(Integer, primary_key=True, index=True)
    winner = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    stage = Column(String(100), nullable=False, index=True)
    team1 = Column(String(255), nullable=False)
    team2 = Column(String(255), nullable=False)

    is_selected = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # New fields for CRUD

    post_id = Column(String(255), nullable=True, unique=True)
    team_1_goal = Column(Integer, nullable=True)
    team_2_goal = Column(Integer, nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    usergmail = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)







