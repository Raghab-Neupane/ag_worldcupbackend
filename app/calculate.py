from fastapi import APIRouter, status, Depends, HTTPException
from typing import Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Match

router = APIRouter(prefix="/calculate", tags=["calculate"])

@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
def health_check():
    """Simple health check for the calculate service"""
    return {"status": "ok"}


class CalculatePayload(BaseModel):
    post_id: Optional[int] = None
    team_1_name: str
    team_1_goal: Optional[int] = None
    team_2_name: str
    team_2_goal: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

@router.post("/", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def calculate(payload: CalculatePayload):
    """Perform calculation without persisting to the database."""
    # Echo back the payload with a success message.
    result = {
        "message": "Calculation received",
        "payload": payload.dict() if hasattr(payload, "dict") else payload,
    }
    return result
