
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.models import Plan
from app.schemas import PlanCreate, PlanUpdate, PlanResponse, PlanListResponse

router = APIRouter()


@router.post("/", response_model=PlanResponse, status_code=201)
def create_plan(plan: PlanCreate, db: Session = Depends(get_db)):
    """Create a new subscription plan"""
    existing_plan = db.query(Plan).filter(Plan.name == plan.name).first()
    if existing_plan:
        raise HTTPException(status_code=400, detail="Plan name already exists")
    
    db_plan = Plan(
        name=plan.name,
        price=plan.price,
        duration_days=plan.duration_days
    )
    
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    
    return db_plan


@router.get("/", response_model=PlanListResponse)
def get_plans(
    is_active: Optional[bool] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    """Get list of all plans with optional filtering"""
    
    query = db.query(Plan)
    
    if is_active is not None:
        query = query.filter(Plan.is_active == ("active" if is_active else "inactive"))
    
    if min_price is not None:
        query = query.filter(Plan.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Plan.price <= max_price)
    
    total = query.count()
    plans = query.all()
    
    return {"total": total, "items": plans}


@router.get("/{plan_id}", response_model=PlanResponse)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.put("/{plan_id}", response_model=PlanResponse)
def update_plan(plan_id: int, plan_update: PlanUpdate, db: Session = Depends(get_db)):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    if plan_update.name and plan_update.name != plan.name:
        existing = db.query(Plan).filter(Plan.name == plan_update.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Plan name already exists")
    
    update_data = plan_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plan, field, value)
    
    plan.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(plan)
    
    return plan


@router.delete("/{plan_id}", status_code=204)
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    plan.is_active = "inactive"
    plan.updated_at = datetime.utcnow()
    db.commit()
    return None
