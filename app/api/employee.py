from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import AuthService
from app.repository.employee import EmployeeRepository
from app.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate, EmployeeSkill, EmployeeSkillCreate, EmployeeLeave, EmployeeLeaveCreate
from typing import List

router = APIRouter()

@router.post("/", response_model=Employee, summary="Create Employee Record")
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    user_role: str = Depends(AuthService.verify_user_access)
):
    """
    **Create New Employee Record**
    
    Creates comprehensive employee record in the database.
    **Available to all authenticated users.**
    
    **Required Header:**
    - `X-User-Role`: Your business role
    """
    try:
        repo = EmployeeRepository(db)
        return repo.create_employee(employee)
    except Exception as e:
        return {"error": "Employee creation not available"}