from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal

class EmployeeBase(BaseModel):
    employee_id: str
    first_name: str
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    display_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None
    nationality: Optional[str] = None
    
    # Contact Information
    primary_email: EmailStr
    secondary_email: Optional[EmailStr] = None
    mobile_phone: Optional[str] = None
    work_phone: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    
    # Address Information
    current_address: Optional[str] = None
    permanent_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    
    # Employment Information
    hire_date: Optional[date] = None
    employment_type: Optional[str] = "Full-Time"
    employment_status: Optional[str] = "Active"
    termination_date: Optional[date] = None
    last_working_day: Optional[date] = None
    probation_end_date: Optional[date] = None
    
    # Job Information
    job_title: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    business_role: str
    reporting_manager_id: Optional[int] = None
    
    # Compensation
    salary: Optional[Decimal] = None
    currency: Optional[str] = "USD"
    pay_grade: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    primary_email: Optional[EmailStr] = None
    mobile_phone: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    business_role: Optional[str] = None
    employment_status: Optional[str] = None
    salary: Optional[Decimal] = None

class Employee(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class EmployeeSkillBase(BaseModel):
    skill_name: str
    proficiency_level: str
    years_of_experience: Optional[int] = None
    certified: Optional[bool] = False

class EmployeeSkillCreate(EmployeeSkillBase):
    employee_id: int

class EmployeeSkill(EmployeeSkillBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    employee_id: int

class EmployeeLeaveBase(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    days_count: int
    reason: Optional[str] = None

class EmployeeLeaveCreate(EmployeeLeaveBase):
    employee_id: int

class EmployeeLeave(EmployeeLeaveBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    employee_id: int
    status: str
    applied_date: datetime

class DepartmentBase(BaseModel):
    department_name: str
    department_code: str
    head_of_department: Optional[int] = None
    budget: Optional[Decimal] = None
    location: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool