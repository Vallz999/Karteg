from flask import request
from models.transaksi_model import TransaksiModel
from models.detail_pesanan_model import DetailPesananModel
from database.db import fetch_all
from utils.validator import validate_date_filter
from utils.helper import (
    success_response,
    validation_error
)

def get_all_riwayat():
    """Mengambil semua riwayat transaksi"""
    return success_response(
        data=TransaksiModel.get_all()
    )

def get_detail_riwayat(id_transaksi):
    """
    Mengambil detail item dari satu transaksi tertentu.
    Data dibungkus dalam objek dengan key 'detail' agar 
    sinkron dengan mapping data.detail di frontend (riwayat.js).
    """
    items = DetailPesananModel.get_by_transaksi(id_transaksi)
    
    response_data = {
        "id_transaksi": id_transaksi,
        "detail": items if items is not None else []
    }
    
    return success_response(
        data=response_data
    )

def filter_by_date():
    """Menyaring riwayat transaksi berdasarkan rentang tanggal"""
    start = request.args.get("start")
    end = request.args.get("end")

    errors = validate_date_filter(
        start,
        end
    )

    if errors:
        return validation_error(errors)

    data = fetch_all("""
        SELECT *
        FROM transaksi
        WHERE DATE(tanggal)
        BETWEEN %s AND %s
        ORDER BY tanggal DESC
    """, (
        start,
        end
    ))

    return success_response(
        data=data
    )