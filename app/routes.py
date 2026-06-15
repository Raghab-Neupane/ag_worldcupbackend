from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import MatchCreate, MatchResponse, SelectedMatchUpdate
from app.services import (
    create_match,
    delete_match,
    get_match,
    list_matches,
    update_match_details,
    get_selected_match,
    set_selected_match,
)


router = APIRouter(prefix="/matches", tags=["matches"])


@router.post("", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
def add_match(payload: MatchCreate, db: Session = Depends(get_db)):
    try:
        return create_match(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[MatchResponse])
def get_all_matches(db: Session = Depends(get_db)):
    return list_matches(db)






@router.get("/selectedmatch", response_model=MatchResponse)
def get_selected_match_endpoint(db: Session = Depends(get_db)):
    match = get_selected_match(db)
    if not match:
        raise HTTPException(status_code=404, detail="Selected match not found")
    return match


@router.patch("/selectedmatch/{match_no}", response_model=MatchResponse)
def update_selected_match_endpoint(match_no: int, payload: SelectedMatchUpdate, db: Session = Depends(get_db)):
    try:
        return set_selected_match(db, match_no, payload.winner, payload.phone)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{match_no}")
def remove_match(match_no: int, db: Session = Depends(get_db)):
    match = get_match(db, match_no)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    delete_match(db, match)
    return {"match_no": match_no}


@router.put("/{match_no}", response_model=MatchResponse)
def update_match(match_no: int, payload: MatchCreate, db: Session = Depends(get_db)):
    match = get_match(db, match_no)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return update_match_details(db, match, payload)
