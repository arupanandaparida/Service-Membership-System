
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from datetime import date, datetime

from app.database import get_db
from app.models import Member
from app.schemas import MemberCreate, MemberUpdate, MemberResponse, MemberListResponse

router = APIRouter()


@router.post("/", response_model=MemberResponse, status_code=201)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):

    # Check if phone already exists
    existing_member = db.query(Member).filter(Member.phone == member.phone).first()
    if existing_member:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    # Create new member
    db_member = Member(
        name=member.name,
        phone=member.phone,
        status=member.status,
        join_date=member.join_date or date.today()
    )
    
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    
    return db_member


@router.get("/", response_model=MemberListResponse)
def get_members(
    status: Optional[str] = Query(None, description="Filter by status (active/inactive/suspended)"),
    search: Optional[str] = Query(None, description="Search by name or phone"),
    db: Session = Depends(get_db)
):
    """
    Get list of all members with optional filtering
    
    - **status**: Filter by member status
    - **search**: Search members by name or phone
    """
    query = db.query(Member)
    
    # Apply status filter
    if status:
        if status not in ['active', 'inactive', 'suspended']:
            raise HTTPException(status_code=400, detail="Invalid status value")
        query = query.filter(Member.status == status)
    
    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Member.name.ilike(search_pattern),
                Member.phone.ilike(search_pattern)
            )
        )

    # Total count
    total = query.count()

    # Fetch ALL results (no pagination)
    members = query.all()
    
    return {
        "total": total,
        "items": members
    }


@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    """
    Get a specific member by ID
    """
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member





@router.delete("/{member_id}", status_code=204)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    """
    Delete a member (soft delete by setting status to inactive)
    """
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Soft delete
    member.status = "inactive"
    member.updated_at = datetime.utcnow()
    
    db.commit()
    
    return None
