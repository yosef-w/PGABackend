from database import Base, engine
import models


def reset_database():
    """Drop all tables and recreate them from models."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
    print("Database has been reset.")
