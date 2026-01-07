from sqlalchemy.orm import Session
from app.models.employee import Employee, EmployeeSkill, EmployeeLeave, Department
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeSkillCreate, EmployeeLeaveCreate
from typing import Optional, List

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_employee(self, employee: EmployeeCreate) -> Employee:
        db_employee = Employee(**employee.model_dump())
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee
    
    def get_employee_by_id(self, employee_id: int) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.id == employee_id).first()
    
    def get_employee_by_emp_id(self, emp_id: str) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.employee_id == emp_id).first()
    
    def get_employees_by_department(self, department: str) -> List[Employee]:
        return self.db.query(Employee).filter(Employee.department == department).all()
    
    def get_employees_by_role(self, role: str) -> List[Employee]:
        return self.db.query(Employee).filter(Employee.business_role == role).all()
    
    def get_all_employees(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        return self.db.query(Employee).filter(Employee.is_active == True).offset(skip).limit(limit).all()
    
    def update_employee(self, employee_id: int, update_data: EmployeeUpdate) -> Optional[Employee]:
        employee = self.get_employee_by_id(employee_id)
        if employee:
            for field, value in update_data.model_dump(exclude_unset=True).items():
                setattr(employee, field, value)
            self.db.commit()
            self.db.refresh(employee)
        return employee
    
    def deactivate_employee(self, employee_id: int) -> bool:
        employee = self.get_employee_by_id(employee_id)
        if employee:
            employee.is_active = False
            employee.employment_status = "Terminated"
            self.db.commit()
            return True
        return False
    
    def add_employee_skill(self, skill: EmployeeSkillCreate) -> EmployeeSkill:
        db_skill = EmployeeSkill(**skill.model_dump())
        self.db.add(db_skill)
        self.db.commit()
        self.db.refresh(db_skill)
        return db_skill
    
    def create_leave_request(self, leave: EmployeeLeaveCreate) -> EmployeeLeave:
        db_leave = EmployeeLeave(**leave.model_dump())
        self.db.add(db_leave)
        self.db.commit()
        self.db.refresh(db_leave)
        return db_leave