from app.core.database import engine, Base
from app.models.identity import Identity, TargetApplication

def create_tables():
    # Drop existing tables to recreate with new schema
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database tables updated successfully with comprehensive Identity model!")

if __name__ == "__main__":
    create_tables()