from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


RESULT_VALUES = {"TEAM1", "TEAM2", "DRAW"}
STATUS_VALUES = {"upcoming", "completed"}


class MatchBase(BaseModel):
    match_no: int = Field(..., ge=1)
    stage: str = Field(..., min_length=1)
    team1: str = Field(..., min_length=1)
    team2: str = Field(..., min_length=1)
    result: Optional[str] = None
    winner: Optional[str] = None
    status: Optional[str] = "upcoming"
    phone: Optional[str] = None

    @field_validator("stage", "team1", "team2")
    @classmethod
    def not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value

    @field_validator("result")
    @classmethod
    def validate_result(cls, value: Optional[str]) -> Optional[str]:
        if value == "":
            return None
        if value is not None and value not in RESULT_VALUES:
            raise ValueError("invalid result value")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: Optional[str]) -> Optional[str]:
        if value == "":
            return "upcoming"
        if value is not None and value not in STATUS_VALUES:
            raise ValueError("invalid status value")
        return value

    @model_validator(mode="after")
    def validate_teams(self):
        if self.team1 == self.team2:
            raise ValueError("team1 and team2 must be different")
        return self


class MatchCreate(MatchBase):
    pass


class MatchBulkCreate(BaseModel):
    matches: List[MatchCreate]


class MatchResultUpdate(BaseModel):
    result: Optional[str] = None

    @field_validator("result")
    @classmethod
    def validate_result(cls, value: Optional[str]) -> Optional[str]:
        if value == "":
            return None
        if value is not None and value not in RESULT_VALUES:
            raise ValueError("invalid result value")
        return value


class MatchStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in STATUS_VALUES:
            raise ValueError("invalid status value")
        return value


class MatchResponse(BaseModel):
    match_no: int
    stage: str
    team1: str
    team2: str
    result: Optional[str] = None
    winner: Optional[str] = None
    status: str
    phone: Optional[str] = None
    is_selected: bool = False

    model_config = {"from_attributes": True}

class SelectedMatchUpdate(BaseModel):
    winner: Optional[str] = None
    phone: Optional[str] = None

class APIResponse(BaseModel):
    success: bool = True
    message: str = "Operation successful"
    data: Dict[str, Any] = Field(default_factory=dict)
