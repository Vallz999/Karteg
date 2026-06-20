from flask import request, session

from services.transaksi_service import (
    create_transaction,
    get_default_pesanan
)

from models.lauk_model import LaukModel

from utils.validator import validate_transaksi

from utils.helper import (
    success_response,
    validation_error,
    error_response
)


# karteg_backend/controllers/transaksi_controller.py

def get_available_lauk():
    """
    Mengambil seluruh lauk (termasuk yang habis) 
    untuk diproses filter & tampilannya di frontend.
    """
    # GANTI: dari LaukModel.get_available() menjadi LaukModel.get_all()
    return success_response(
        data=LaukModel.get_all()
    )


def get_default_nasi():
    """
    Mengambil data nasi default
    yang otomatis muncul pada
    detail pesanan.
    """

    try:

        default_nasi = get_default_pesanan()

        return success_response(
            data=default_nasi
        )

    except Exception as e:

        return error_response(
            f"Gagal mengambil data nasi default: {str(e)}"
        )


def create_transaksi():
    """
    Membuat transaksi baru
    beserta pesanan nasi dan
    detail lauk yang dipilih.
    """

    try:

        data = request.json

        if not data:
            return error_response(
                "Data transaksi tidak ditemukan"
            )

        errors = validate_transaksi(data)

        if errors:
            return validation_error(errors)

        # ==================================================
        # Default nasi otomatis jika tidak dikirim frontend
        # ==================================================

        if "jumlah_nasi" not in data:
            data["jumlah_nasi"] = 1

        if "harga_nasi" not in data:
            data["harga_nasi"] = 5000

        result = create_transaction(
            session["user_id"],
            data
        )

        if not result["status"]:

            return error_response(
                result["message"]
            )

        return success_response(
            "Transaksi berhasil",
            {
                "id_transaksi":
                    result["transaksi_id"]
            }
        )

    except Exception as e:

        return error_response(
            f"Gagal membuat transaksi: {str(e)}"
        )