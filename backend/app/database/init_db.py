
from app.database.connection import Base, engine
from app.models.repository import Repository
from app.models.analysis import Analysis

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
