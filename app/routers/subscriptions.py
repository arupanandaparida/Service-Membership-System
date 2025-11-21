
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, timedelta, datetime
from typing import Optional

from app.database import get_db
from app.models import Subscription, Member, Plan
from app.schemas import SubscriptionCreate, SubscriptionResponse

router = APIRouter()


@router.post("/", response_model=SubscriptionResponse, status_code=201)
def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):

    # Validate member exists
    member = db.query(Member).filter(Member.id == subscription.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Validate plan exists
    plan = db.query(Plan).filter(Plan.id == subscription.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Check if plan is active
    if plan.is_active != "active":
        raise HTTPException(status_code=400, detail="Cannot subscribe to inactive plan")
    
    # Calculate end date
    end_date = subscription.start_date + timedelta(days=plan.duration_days)
    
    # Create subscription
    db_subscription = Subscription(
        member_id=subscription.member_id,
        plan_id=subscription.plan_id,
        start_date=subscription.start_date,
        end_date=end_date,
        status="active"
    )
    
    db.add(db_subscription)
    
    # Update member status to active if creating new subscription
    if member.status != "active":
        member.status = "active"
        member.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_subscription)
    
    return db_subscription


@router.get("/members/{member_id}/current-subscription", response_model=SubscriptionResponse)
def get_current_subscription(member_id: int, db: Session = Depends(get_db)):

    # Validate member exists
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Get current date
    today = date.today()
    
    # Find active subscription
    subscription = db.query(Subscription).filter(
        Subscription.member_id == member_id,
        Subscription.start_date <= today,
        Subscription.end_date >= today,
        Subscription.status == "active"
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="No active subscription found for this member"
        )
    
    return subscription


@router.get("/", response_model=list[SubscriptionResponse])
def get_all_subscriptions(
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get all subscriptions with optional filtering
    """
    query = db.query(Subscription)
    
    if status:
        if status not in ['active', 'expired', 'cancelled']:
            raise HTTPException(status_code=400, detail="Invalid status value")
        query = query.filter(Subscription.status == status)
    
    subscriptions = query.order_by(Subscription.created_at.desc()).offset(skip).limit(limit).all()
    
    return subscriptions


@router.put("/{subscription_id}/cancel", response_model=SubscriptionResponse)
def cancel_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """
    Cancel a subscription
    """
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    if subscription.status == "cancelled":
        raise HTTPException(status_code=400, detail="Subscription already cancelled")
    
    subscription.status = "cancelled"
    subscription.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(subscription)
    
    return subscription