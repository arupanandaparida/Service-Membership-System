
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date

from app.database import get_db
from app.models import Attendance, Member, Subscription
from app.schemas import AttendanceCheckIn, AttendanceResponse, AttendanceListResponse

router = APIRouter()

@router.post("/check-in", response_model=AttendanceResponse, status_code=201)
def check_in(check_in_data: AttendanceCheckIn, db: Session = Depends(get_db)):

    member = db.query(Member).filter(Member.id == check_in_data.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    today = date.today()

    active_subscription = db.query(Subscription).filter(
        Subscription.member_id == member.id,
        Subscription.start_date <= today,
        Subscription.end_date >= today,
        Subscription.status == "active"
    ).first()

    if not active_subscription:
        raise HTTPException(
            status_code=400,
            detail="No active subscription for this member"
        )

    attendance = Attendance(
        member_id=member.id,
        check_in_time=datetime.utcnow()
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return attendance


@router.get("/members/{member_id}/attendance", response_model=AttendanceListResponse)
def get_member_attendance(member_id: int, db: Session = Depends(get_db)):
    """
    Return ALL attendance records for a given member.
    No filters. No pagination.
    """
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    records = db.query(Attendance).filter(
        Attendance.member_id == member_id
    ).order_by(Attendance.check_in_time.desc()).all()

    return {
        "total": len(records),
        "items": records
    }
