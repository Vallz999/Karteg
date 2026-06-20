from flask import request
from models.lauk_model import LaukModel
from utils.validator import validate_lauk
from utils.helper import (
    success_response,
    validation_error
)


def get_all_lauk():
    return success_response(
        data=LaukModel.get_all()
    )


def create_lauk():
    data = request.json

    errors = validate_lauk(data)

    if errors:
        return validation_error(errors)

    LaukModel.create(
        data["nama_lauk"],
        data["harga"],
        data["stok"],
        data["status"],
        data["id_kategori"]
    )

    return success_response(
        "Lauk berhasil ditambahkan"
    )


def update_lauk(id_lauk):
    data = request.json

    errors = validate_lauk(data)

    if errors:
        return validation_error(errors)

    LaukModel.update(
        id_lauk,
        data["nama_lauk"],
        data["harga"],
        data["stok"],
        data["status"],
        data["id_kategori"]
    )

    return success_response(
        "Lauk berhasil diupdate"
    )


def delete_lauk(id_lauk):
    LaukModel.delete(id_lauk)

    return success_response(
        "Lauk berhasil dihapus"
    )


def update_stok(id_lauk):
    data = request.json

    LaukModel.update_stok(
        id_lauk,
        data["stok"]
    )

    return success_response(
        "Stok berhasil diupdate"
    )


def update_status(id_lauk):
    data = request.json

    LaukModel.update_status(
        id_lauk,
        data["status"]
    )

    return success_response(
        "Status berhasil diupdate"
    )