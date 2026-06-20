from flask import session, jsonify
from functools import wraps


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if "role" not in session:
            return jsonify({
                "status": "error",
                "message": "Silakan login terlebih dahulu."
            }), 401

        if session["role"] != "admin":
            return jsonify({
                "status": "error",
                "message": "Akses hanya untuk admin."
            }), 403

        return f(*args, **kwargs)

    return wrapper


def kasir_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if "role" not in session:
            return jsonify({
                "status": "error",
                "message": "Silakan login terlebih dahulu."
            }), 401

        if session["role"] not in ["kasir", "admin"]:
            return jsonify({
                "status": "error",
                "message": "Akses hanya untuk kasir/admin."
            }), 403

        return f(*args, **kwargs)

    return wrapper