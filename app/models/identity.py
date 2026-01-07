from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Identity(Base):
    __tablename__ = "identities"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    employee_id = Column(String, unique=True, index=True)
    external_id = Column(String, nullable=True)
    
    # Basic Identity Information
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    display_name = Column(String)
    
    # Contact Information
    primary_email = Column(String, unique=True, index=True)
    secondary_email = Column(String, nullable=True)
    mobile_phone = Column(String, nullable=True)
    work_phone = Column(String, nullable=True)
    
    # Employment Information
    employment_type = Column(String, default="Employee")
    employment_status = Column(String, default="ACTIVE")
    hire_date = Column(Date, nullable=True)
    termination_date = Column(Date, nullable=True)
    last_working_day = Column(Date, nullable=True)
    
    # Organizational Information
    department = Column(String, nullable=True)
    location = Column(String, nullable=True)
    cost_center = Column(String, nullable=True)
    division = Column(String, nullable=True)
    building = Column(String, nullable=True)
    floor = Column(String, nullable=True)
    office = Column(String, nullable=True)
    
    # Job Information
    job_title = Column(String, nullable=True)
    job_code = Column(String, nullable=True)
    job_level = Column(String, nullable=True)
    job_family = Column(String, nullable=True)
    
    # Manager Relationships
    manager_id = Column(Integer, ForeignKey('identities.id'), nullable=True)
    manager_external_id = Column(String, nullable=True)
    reports_to_name = Column(String, nullable=True)
    
    # Security & Compliance
    security_clearance = Column(String, nullable=True)
    background_check_status = Column(String, nullable=True)
    background_check_date = Column(Date, nullable=True)
    
    # Account Status & Lifecycle
    account_status = Column(String, default="ACTIVE")
    lifecycle_state = Column(String, default="ACTIVE")
    risk_score = Column(Integer, default=0)
    
    # Business Role & Entitlements (existing)
    business_role = Column(String, index=True)
    entitlements = Column(JSON)
    is_active = Column(Boolean, default=True)
    
    # Audit Fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, default="system")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_modified_by = Column(String, default="system")
    
    # Relationships
    manager = relationship("Identity", remote_side=[id], backref="direct_reports")

class TargetApplication(Base):
    __tablename__ = "target_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    protocol = Column(String)  # SCIM, REST, etc.
    auth_type = Column(String)  # OAuth, API Key, etc.
    base_url = Column(String)
    config = Column(JSON)
    is_active = Column(Boolean, default=True)