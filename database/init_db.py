from database.db import engine
from database.models import Trade
from database.db import Base

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")


if __name__ == "__main__":
    init_db()