from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Match
from app.schemas import MatchCreate


def match_to_dict(match: Match):
    return {
        "match_no": match.match_no,
        "stage": match.stage,
        "team1": match.team1,
        "team2": match.team2,
        "winner": match.winner,
        "phone": match.phone,
        "post_id": match.post_id,
        "team_1_goal": match.team_1_goal,
        "team_2_goal": match.team_2_goal,
        "start_time": match.start_time,
        "end_time": match.end_time,
        "created_at": match.created_at,
        "updated_at": match.updated_at,
        # Computed field for legacy UI compatibility
        "goal_difference": (f"{match.team_1_goal}-{match.team_2_goal}" if match.team_1_goal is not None and match.team_2_goal is not None else None),
    }


def get_match(db: Session, match_no: int):
    return db.query(Match).filter(Match.match_no == match_no).first()


def list_matches(db: Session):
    return db.query(Match).order_by(Match.match_no.asc()).all()





def list_matches_by_stage(db: Session, stage: str):
    return db.query(Match).filter(Match.stage == stage).order_by(Match.match_no.asc()).all()


def bulk_insert_matches(db: Session, matches: list[MatchCreate]):
    inserted = []
    skipped = []
    try:
        seen_match_nos = set()
        for item in matches:
            if item.match_no in seen_match_nos:
                skipped.append(item.match_no)
                continue
            seen_match_nos.add(item.match_no)
            existing = get_match(db, item.match_no)
            if existing:
                skipped.append(item.match_no)
                continue
            match = Match(
                match_no=item.match_no,
                stage=item.stage,
                team1=item.team1,
                team2=item.team2,
            )
            db.add(match)
            inserted.append(match)
        db.commit()
        for match in inserted:
            db.refresh(match)
        return inserted, skipped
    except IntegrityError:
        db.rollback()
        raise






def delete_match(db: Session, match: Match):
    db.delete(match)
    db.commit()


def create_match(db: Session, item: MatchCreate):
    # If match_no is provided, ensure it does not already exist
    if item.match_no is not None:
        existing = get_match(db, item.match_no)
        if existing:
            raise ValueError("Match number already exists")
    # Build Match instance, only include match_no if present
    match_data = {
        "stage": item.stage,
        "team1": item.team1,
        "team2": item.team2,
        "post_id": item.post_id,
        "team_1_goal": item.team_1_goal,
        "team_2_goal": item.team_2_goal,
        "start_time": item.start_time,
        "end_time": item.end_time,
    }
    if item.match_no is not None:
        match_data["match_no"] = item.match_no
    match = Match(**match_data)
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

def update_match_details(db: Session, match: Match, item: MatchCreate):
    match.stage = item.stage
    match.team1 = item.team1
    match.team2 = item.team2
    match.post_id = item.post_id
    # Convert empty strings to None and cast to int for goal fields
    if item.team_1_goal in (None, ''):
        match.team_1_goal = None
    else:
        match.team_1_goal = int(item.team_1_goal)
    if item.team_2_goal in (None, ''):
        match.team_2_goal = None
    else:
        match.team_2_goal = int(item.team_2_goal)
    match.start_time = item.start_time
    match.end_time = item.end_time
    db.commit()
    db.refresh(match)
    return match


# Selected match helpers

def get_selected_match(db: Session):
    """Return the match currently marked as selected."""
    return db.query(Match).filter(Match.is_selected == True).first()

def set_selected_match(db: Session, match_id: int, winner: Optional[str] = None, phone: Optional[str] = None):
    """Set a single match as selected, deselect others, and optionally update winner and phone.
    This operation is performed within a transaction to ensure atomicity.
    """
    # Deselect any previously selected match
    db.query(Match).filter(Match.is_selected == True).update({Match.is_selected: False})
    # Fetch the target match
    match = db.query(Match).filter(Match.match_no == match_id).first()
    if not match:
        raise ValueError(f"Match with id {match_id} not found")
    match.is_selected = True
    if winner is not None:
        match.winner = winner
    if phone is not None:
        match.phone = phone
    db.commit()
    db.refresh(match)
    return match
