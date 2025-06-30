from database import Base, engine


def reset_db() -> None:
    """Drop and recreate all tables."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_db()
    print("Database cleared and recreated.")
