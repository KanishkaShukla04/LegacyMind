from app.database.connection import Base

def get_db():
    from app.database.connection import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
