import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import User
from app.crud import create_user, get_user_by_email
from app.schemas import UserCreate

DATABASE_URL = "sqlite:///:memory:"

class TestCRUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine = create_engine(DATABASE_URL)
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        cls.db = TestingSessionLocal()
        Base.metadata.create_all(bind=engine)

    def test_create_user(self):
        user_data = UserCreate(email="test@example.com", password="password123")
        user = create_user(self.db, user_data)
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.hashed_password)

    def test_get_user_by_email(self):
        user = get_user_by_email(self.db, "test@example.com")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")

if __name__ == "__main__":
    unittest.main()
