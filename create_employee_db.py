from app.core.database import engine, Base
from app.models.identity import Identity, TargetApplication
from app.models.employee import Employee, EmployeeDocument, EmployeeSkill, EmployeeLeave, EmployeePerformance, Department

def create_all_tables():
    # Drop existing tables to recreate with new schema
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("All database tables created successfully!")
    print("Tables created:")
    print("- identities (Identity Management)")
    print("- target_applications (Target Apps)")
    print("- employees (Employee Records)")
    print("- employee_documents (Employee Documents)")
    print("- employee_skills (Employee Skills)")
    print("- employee_leaves (Leave Management)")
    print("- employee_performance (Performance Reviews)")
    print("- departments (Department Management)")

if __name__ == "__main__":
    create_all_tables()