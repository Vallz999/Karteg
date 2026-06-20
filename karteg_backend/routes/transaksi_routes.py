from flask import Blueprint

from controllers.transaksi_controller import (
    create_transaksi,
    get_available_lauk,
    get_default_nasi
)

from middleware.auth_middleware import (
    login_required
)

from middleware.role_middleware import (
    kasir_required
)

transaksi_bp = Blueprint(
    "transaksi",
    __name__
)


# =====================================
# GET LAUK TERSEDIA
# =====================================

transaksi_bp.route(
    "/lauk",
    methods=["GET"]
)(
    login_required(
        kasir_required(
            get_available_lauk
        )
    )
)


# =====================================
# GET DEFAULT PESANAN (NASI)
# =====================================

transaksi_bp.route(
    "/default",
    methods=["GET"]
)(
    login_required(
        kasir_required(
            get_default_nasi
        )
    )
)


# =====================================
# SIMPAN TRANSAKSI
# =====================================

transaksi_bp.route(
    "/",
    methods=["POST"]
)(
    login_required(
        kasir_required(
            create_transaksi
        )
    )
)