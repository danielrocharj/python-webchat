from app.database.core import SessionLocal
from app.database.seeder import user_seeder


def main():
    db = SessionLocal()
    user_seeder(db)


if __name__ == "__main__":
    main()
