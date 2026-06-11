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
        "result": match.result,
        "winner": match.winner,
        "status": match.status,
        "phone": match.phone,
        "created_at": match.created_at,
        "updated_at": match.updated_at,
    }


def get_match(db: Session, match_no: int):
    return db.query(Match).filter(Match.match_no == match_no).first()


def list_matches(db: Session):
    return db.query(Match).order_by(Match.match_no.asc()).all()


def list_matches_by_status(db: Session, status: str):
    return db.query(Match).filter(Match.status == status).order_by(Match.match_no.asc()).all()


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
                result=item.result,
                winner=item.winner,
                status=item.status or "upcoming",
                phone=item.phone,
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


def update_match_result(db: Session, match: Match, result: str):
    match.result = result if result else None
    db.commit()
    db.refresh(match)
    return match


def update_match_status(db: Session, match: Match, status: str):
    match.status = status
    db.commit()
    db.refresh(match)
    return match


def delete_match(db: Session, match: Match):
    db.delete(match)
    db.commit()


def create_match(db: Session, item: MatchCreate):
    existing = get_match(db, item.match_no)
    if existing:
        raise ValueError("Match number already exists")
    match = Match(
        match_no=item.match_no,
        stage=item.stage,
        team1=item.team1,
        team2=item.team2,
        result=item.result,
        winner=item.winner,
        status=item.status or "upcoming",
        phone=item.phone,
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

def update_match_details(db: Session, match: Match, item: MatchCreate):
    match.stage = item.stage
    match.team1 = item.team1
    match.team2 = item.team2
    match.result = item.result
    match.winner = item.winner
    match.status = item.status or "upcoming"
    match.phone = item.phone
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
