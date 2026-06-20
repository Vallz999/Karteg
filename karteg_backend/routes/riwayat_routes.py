from flask import Blueprint
from controllers.riwayat_controller import (
    get_all_riwayat,
    get_detail_riwayat,
    filter_by_date
)
from middleware.auth_middleware import login_required
from middleware.role_middleware import kasir_required  # Sekarang mengizinkan kasir & admin

riwayat_bp = Blueprint("riwayat", __name__)

# Mengambil semua riwayat (Bisa diakses Admin & Kasir)
riwayat_bp.route("/", methods=["GET"])(
    login_required(
        kasir_required(
            get_all_riwayat
        )
    )
)

# Mengambil detail satu riwayat (Bisa diakses Admin & Kasir)
riwayat_bp.route("/<int:id_transaksi>", methods=["GET"])(
    login_required(
        kasir_required(
            get_detail_riwayat
        )
    )
)

# Filter riwayat berdasarkan tanggal (Bisa diakses Admin & Kasir)
riwayat_bp.route("/filter", methods=["GET"])(
    login_required(
        kasir_required(
            filter_by_date
        )
    )
)