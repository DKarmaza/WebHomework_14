import unittest
from app.auth import get_password_hash, verify_password, create_access_token
from jose import jwt
import time

SECRET_KEY = "testsecretkey"
ALGORITHM = "HS256"

class TestAuth(unittest.TestCase):
    def test_password_hashing(self):
        password = "password123"
        hashed_password = get_password_hash(password)
        self.assertTrue(verify_password(password, hashed_password))

    def test_jwt_token_creation(self):
        data = {"sub": "test@example.com"}
        token = create_access_token(data, expires_delta=None)
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(decoded["sub"], "test@example.com")
        self.assertIn("exp", decoded)

    def test_expired_jwt(self):
        data = {"sub": "test@example.com"}
        token = create_access_token(data, expires_delta=-1)
        time.sleep(2)
        with self.assertRaises(jwt.ExpiredSignatureError):
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

if __name__ == "__main__":
    unittest.main()
