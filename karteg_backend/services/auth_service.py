import bcrypt
from database.db import fetch_one
from models.user_model import UserModel
from utils.hash import hash_password

def register_user(username, password, role="kasir"):

    existing = UserModel.find_by_username(
        username
    )

    if existing:
        return {
            "status": False,
            "message": "Username sudah digunakan"
        }

    hashed = hash_password(password)

    UserModel.create(
        username,
        hashed,
        role
    )

    return {
        "status": True
    }

def authenticate_user(username, password):
    user = fetch_one(
        "SELECT * FROM user WHERE username=%s",
        (username,)
    )

    if not user:
        return None

    print("INPUT:", password)
    print("DB HASH:", user["password"])

    valid = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"].encode("utf-8")
    )

    print("VALID:", valid)

    if valid:
        return user

    return None


def get_user_by_username(username):
    return fetch_one(
        "SELECT * FROM user WHERE username=%s",
        (username,)
    )


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")