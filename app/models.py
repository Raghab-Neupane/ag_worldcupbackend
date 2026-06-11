from sqlalchemy import Column, DateTime, Enum, Index, Integer, String, Boolean, func

from app.database import Base


RESULT_VALUES = ("TEAM1", "TEAM2", "DRAW")
STATUS_VALUES = ("upcoming", "live", "completed")


class Match(Base):
    __tablename__ = "matches"

    match_no = Column(Integer, primary_key=True, index=True)
    stage = Column(String(100), nullable=False, index=True)
    team1 = Column(String(255), nullable=False)
    team2 = Column(String(255), nullable=False)
    result = Column(Enum(*RESULT_VALUES, name="match_result"), nullable=True)
    winner = Column(String(255), nullable=True)
    status = Column(Enum(*STATUS_VALUES, name="match_status"), nullable=False, default="upcoming", index=True)
    phone = Column(String(255), nullable=True)
    is_selected = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


