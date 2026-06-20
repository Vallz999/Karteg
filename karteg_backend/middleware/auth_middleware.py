from flask import session, jsonify
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return jsonify({
                "status": "error",
                "message": "Akses ditolak. Silakan login terlebih dahulu."
            }), 401

        return f(*args, **kwargs)

    return wrapper