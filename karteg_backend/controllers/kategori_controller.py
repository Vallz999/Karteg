from flask import request
from models.kategori_model import KategoriModel
from utils.validator import validate_kategori
from utils.helper import (
    success_response,
    validation_error
)


def get_all_kategori():
    return success_response(
        data=KategoriModel.get_all()
    )


def create_kategori():
    data = request.json

    errors = validate_kategori(data)

    if errors:
        return validation_error(errors)

    KategoriModel.create(
        data["nama_kategori"]
    )

    return success_response(
        "Kategori berhasil ditambahkan"
    )


def update_kategori(id_kategori):
    data = request.json

    errors = validate_kategori(data)

    if errors:
        return validation_error(errors)

    KategoriModel.update(
        id_kategori,
        data["nama_kategori"]
    )

    return success_response(
        "Kategori berhasil diupdate"
    )


def delete_kategori(id_kategori):
    KategoriModel.delete(id_kategori)

    return success_response(
        "Kategori berhasil dihapus"
    )