from flask import request, session
from services.auth_service import authenticate_user
from utils.validator import validate_login
from utils.helper import (
    success_response,
    error_response,
    validation_error
)
from services.auth_service import (
    authenticate_user,
    register_user
)

def register():

    data = request.json

    errors = validate_login(data)

    if errors:
        return validation_error(errors)

    role = data.get("role", "kasir")

    result = register_user(
        data["username"],
        data["password"],
        role
    )

    if not result["status"]:
        return error_response(
            result["message"]
        )

    return success_response(
        "User berhasil dibuat"
    )


def login():
    data = request.json

    errors = validate_login(data)

    if errors:
        return validation_error(errors)

    user = authenticate_user(
        data["username"],
        data["password"]
    )

    if not user:
        return error_response(
            "Username atau password salah",
            401
        )

    session["user_id"] = user["id_user"]
    session["role"] = user["role"]

    return success_response(
        "Login berhasil",
        {
            "role": user["role"]
        }
    )


def logout():
    session.clear()

    return success_response(
        "Logout berhasil"
    )


def check_session():

    if "user_id" not in session:
        return error_response(
            "Belum login",
            401
        )

    return success_response(
        data={
            "user_id": session["user_id"],
            "role": session["role"]
        }
    )