from flask import jsonify
from datetime import datetime


def success_response(
    message="Berhasil",
    data=None,
    status_code=200
):
    response = {
        "status": "success",
        "message": message
    }

    if data is not None:
        response["data"] = data

    return jsonify(response), status_code


def error_response(
    message="Terjadi kesalahan",
    status_code=400
):
    return jsonify({
        "status": "error",
        "message": message
    }), status_code


def validation_error(errors):
    return jsonify({
        "status": "error",
        "errors": errors
    }), 422


def format_currency(value):
    return f"Rp {value:,.0f}".replace(",", ".")


def current_date():
    return datetime.now().strftime(
        "%Y-%m-%d"
    )


def current_datetime():
    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )