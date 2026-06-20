from flask import Blueprint

from controllers.dashboard_controller import (
    get_summary,
    get_penjualan_chart,
    get_lauk_terlaris,
    get_stok_habis
)

from middleware.auth_middleware import (
    login_required
)

from middleware.role_middleware import (
    admin_required
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


dashboard_bp.route(
    "/summary",
    methods=["GET"]
)(
    login_required(
        admin_required(
            get_summary
        )
    )
)


dashboard_bp.route(
    "/chart",
    methods=["GET"]
)(
    login_required(
        admin_required(
            get_penjualan_chart
        )
    )
)


dashboard_bp.route(
    "/top-lauk",
    methods=["GET"]
)(
    login_required(
        admin_required(
            get_lauk_terlaris
        )
    )
)


dashboard_bp.route(
    "/stok-habis",
    methods=["GET"]
)(
    login_required(
        admin_required(
            get_stok_habis
        )
    )
)