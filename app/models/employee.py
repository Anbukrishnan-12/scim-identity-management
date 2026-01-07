from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Date, ForeignKey, Text, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Employee(Base):
    __tablename__ = "employees"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    
    # Personal Information
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    middle_name = Column(String)
    display_name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    marital_status = Column(String)
    nationality = Column(String)
    
    # Contact Information
    primary_email = Column(String, unique=True, index=True)
    secondary_email = Column(String)
    mobile_phone = Column(String)
    work_phone = Column(String)
    emergency_contact_name = Column(String)
    emergency_contact_phone = Column(String)
    
    # Address Information
    current_address = Column(Text)
    permanent_address = Column(Text)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    country = Column(String)
    
    # Employment Information
    hire_date = Column(Date)
    employment_type = Column(String, default="Full-Time")  # Full-Time, Part-Time, Contract
    employment_status = Column(String, default="Active")   # Active, Inactive, Terminated
    termination_date = Column(Date)
    last_working_day = Column(Date)
    probation_end_date = Column(Date)
    
    # Job Information
    job_title = Column(String)
    department = Column(String)
    location = Column(String)
    business_role = Column(String, index=True)
    reporting_manager_id = Column(Integer, ForeignKey('employees.id'))
    
    # Compensation
    salary = Column(Numeric(10, 2))
    currency = Column(String, default="USD")
    pay_grade = Column(String)
    
    # System Fields
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String, default="system")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String, default="system")
    
    # Relationships
    manager = relationship("Employee", remote_side=[id], backref="direct_reports")
    
class EmployeeDocument(Base):
    __tablename__ = "employee_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    document_type = Column(String)  # Resume, ID_Proof, Address_Proof, etc.
    document_name = Column(String)
    file_path = Column(String)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    uploaded_by = Column(String)
    
    employee = relationship("Employee", backref="documents")

class EmployeeSkill(Base):
    __tablename__ = "employee_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    skill_name = Column(String)
    proficiency_level = Column(String)  # Beginner, Intermediate, Advanced, Expert
    years_of_experience = Column(Integer)
    certified = Column(Boolean, default=False)
    
    employee = relationship("Employee", backref="skills")

class EmployeeLeave(Base):
    __tablename__ = "employee_leaves"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    leave_type = Column(String)  # Annual, Sick, Maternity, etc.
    start_date = Column(Date)
    end_date = Column(Date)
    days_count = Column(Integer)
    status = Column(String, default="Pending")  # Pending, Approved, Rejected
    reason = Column(Text)
    approved_by = Column(Integer, ForeignKey('employees.id'))
    applied_date = Column(DateTime(timezone=True), server_default=func.now())
    
    employee = relationship("Employee", foreign_keys=[employee_id], backref="leaves")
    approver = relationship("Employee", foreign_keys=[approved_by])

class EmployeePerformance(Base):
    __tablename__ = "employee_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    review_period = Column(String)  # Q1-2024, Annual-2024, etc.
    overall_rating = Column(Numeric(3, 2))  # 1.00 to 5.00
    goals_achieved = Column(Integer)
    total_goals = Column(Integer)
    feedback = Column(Text)
    reviewer_id = Column(Integer, ForeignKey('employees.id'))
    review_date = Column(Date)
    
    employee = relationship("Employee", foreign_keys=[employee_id], backref="performance_reviews")
    reviewer = relationship("Employee", foreign_keys=[reviewer_id])

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String, unique=True)
    department_code = Column(String, unique=True)
    head_of_department = Column(Integer, ForeignKey('employees.id'))
    budget = Column(Numeric(12, 2))
    location = Column(String)
    is_active = Column(Boolean, default=True)
    
    hod = relationship("Employee", backref="headed_departments")