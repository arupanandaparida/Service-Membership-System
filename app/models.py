"""
SQLAlchemy ORM models for database tables
"""
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Member(Base):
    """Member model representing gym/service members"""
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False, unique=True, index=True)
  
    join_date = Column(Date, nullable=False, default=datetime.utcnow().date)
    status = Column(String(20), nullable=False, default="active", index=True)
    total_check_ins = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    subscriptions = relationship("Subscription", back_populates="member", cascade="all, delete-orphan")
    attendances = relationship("Attendance", back_populates="member", cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('active', 'inactive', 'suspended')", name="check_member_status"),
    )


class Plan(Base):
    """Plan model representing subscription plans"""
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    duration_days = Column(Integer, nullable=False)
    is_active = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    subscriptions = relationship("Subscription", back_populates="plan")

    # Constraints
    __table_args__ = (
        CheckConstraint("price >= 0", name="check_plan_price"),
        CheckConstraint("duration_days > 0", name="check_plan_duration"),
    )


class Subscription(Base):
    """Subscription model representing member subscriptions to plans"""
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id", ondelete="RESTRICT"), nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False, index=True)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    member = relationship("Member", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")

    # Constraints
    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="check_subscription_dates"),
        CheckConstraint("status IN ('active', 'expired', 'cancelled')", name="check_subscription_status"),
    )


class Attendance(Base):
    """Attendance model representing member check-ins"""
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False, index=True)
    check_in_time = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    check_out_time = Column(DateTime, nullable=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    member = relationship("Member", back_populates="attendances")