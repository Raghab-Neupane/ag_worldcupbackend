from typing import Any, Dict, List, Optional
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class MatchBase(BaseModel):
    stage: str = Field(..., min_length=1)
    team1: str = Field(..., min_length=1)
    team2: str = Field(..., min_length=1)

    post_id: Optional[str] = None
    team_1_goal: Optional[int] = None
    team_2_goal: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @field_validator("stage", "team1", "team2")
    @classmethod
    def not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value





    @model_validator(mode="after")
    def validate_teams(self):
        if self.team1 == self.team2:
            raise ValueError("team1 and team2 must be different")
        return self


class MatchCreate(MatchBase):
    """Schema for creating a match (optional match_no)."""
    match_no: Optional[int] = None
    # other fields inherited from MatchBase


class MatchBulkCreate(BaseModel):
    matches: List[MatchCreate]





class MatchResponse(BaseModel):
    match_no: int
    stage: str
    team1: str
    team2: str
    is_selected: bool = False
    post_id: Optional[str] = None
    winner: Optional[str] = None
    phone: Optional[str] = None
    team_1_goal: Optional[int] = None
    team_2_goal: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    model_config = {"from_attributes": True}

class SelectedMatchUpdate(BaseModel):
    winner: Optional[str] = None
    phone: Optional[str] = None

class APIResponse(BaseModel):
    success: bool = True
    message: str = "Operation successful"
    data: Dict[str, Any] = Field(default_factory=dict)
