from pydantic import BaseModel
from typing import Optional

class Matches(BaseModel):
    match_number: int
    stage: str
    team1: str
    team2: str
    winner: Optional[str] = None