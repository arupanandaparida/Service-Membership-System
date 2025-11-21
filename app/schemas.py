"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal


# ========== Member Schemas ==========
class MemberBase(BaseModel):
    """Base schema for Member"""
    name: str = Field(..., min_length=1, max_length=100, description="Member name")
    phone: str = Field(..., min_length=10, max_length=20, description="Member phone number")

    status: Optional[str] = Field("active", description="Member status")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v not in ['active', 'inactive', 'suspended']:
            raise ValueError('Status must be active, inactive, or suspended')
        return v


class MemberCreate(MemberBase):
    """Schema for creating a new member"""
    join_date: Optional[date] = Field(None, description="Join date (defaults to today)")


class MemberUpdate(BaseModel):
    """Schema for updating a member"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
   
    status: Optional[str] = None

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in ['active', 'inactive', 'suspended']:
            raise ValueError('Status must be active, inactive, or suspended')
        return v


class MemberResponse(MemberBase):
    """Schema for member response"""
    id: int
    join_date: date
    total_check_ins: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ========== Plan Schemas ==========
class PlanBase(BaseModel):
    """Base schema for Plan"""
    name: str = Field(..., min_length=1, max_length=100)
    price: Decimal = Field(..., ge=0)
    duration_days: int = Field(..., gt=0)


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[Decimal] = Field(None, ge=0)
    duration_days: Optional[int] = Field(None, gt=0)
    is_active: Optional[str] = None


class PlanResponse(PlanBase):
    id: int
    is_active: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True



# ========== Subscription Schemas ==========
class SubscriptionBase(BaseModel):
    """Base schema for Subscription"""
    member_id: int = Field(..., gt=0, description="Member ID")
    plan_id: int = Field(..., gt=0, description="Plan ID")
    start_date: date = Field(..., description="Subscription start date")


class SubscriptionCreate(SubscriptionBase):
    """Schema for creating a new subscription"""
    pass


class SubscriptionResponse(BaseModel):
    """Schema for subscription response"""
    id: int
    member_id: int
    plan_id: int
    start_date: date
    end_date: date
    status: str
    created_at: datetime
    updated_at: datetime
    
    # Nested objects
    member: Optional[MemberResponse] = None
    plan: Optional[PlanResponse] = None

    class Config:
        from_attributes = True


# ========== Attendance Schemas ==========
class AttendanceCheckIn(BaseModel):
    """Schema for check-in request"""
    member_id: int = Field(..., gt=0, description="Member ID")


class AttendanceResponse(BaseModel):
    """Schema for attendance response"""
    id: int
    member_id: int
    check_in_time: datetime
    check_out_time: Optional[datetime]
    notes: Optional[str]
    created_at: datetime
    
    # Nested member info
    member: Optional[MemberResponse] = None

    class Config:
        from_attributes = True


# ========== Error Response Schema ==========
class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str
    error_code: Optional[str] = None


# ========== List Response Schemas ==========
class MemberListResponse(BaseModel):
    """Schema for paginated member list"""
    total: int
    items: List[MemberResponse]


class PlanListResponse(BaseModel):
    """Schema for paginated plan list"""
    total: int
    items: List[PlanResponse]


class AttendanceListResponse(BaseModel):
    """Schema for paginated attendance list"""
    total: int
    items: List[AttendanceResponse]