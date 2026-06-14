from pydantic import BaseModel
from typing import Optional

class Matches(BaseModel):
    match_number: int
    stage: str
    team1: str
    team2: str

class Result(BaseModel):
    match_number: int
    stage: str
    team1: str
    team2: str
    draw: Optional[bool] = False
    winner_name: str
    winner_number: str
    