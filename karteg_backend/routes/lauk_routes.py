from flask import Blueprint

from controllers.lauk_controller import (
    get_all_lauk,
    create_lauk,
    update_lauk,
    delete_lauk,
    update_stok,
    update_status
)

from middleware.auth_middleware import (
    login_required
)

from middleware.role_middleware import (
    admin_required,
    kasir_required
)

lauk_bp = Blueprint(
    "lauk",
    __name__
)


lauk_bp.route(
    "/",
    methods=["GET"]
)(
    login_required(
        kasir_required(
            get_all_lauk
        )
    )
)


lauk_bp.route(
    "/",
    methods=["POST"]
)(
    login_required(
        admin_required(
            create_lauk
        )
    )
)


lauk_bp.route(
    "/<int:id_lauk>",
    methods=["PUT"]
)(
    login_required(
        admin_required(
            update_lauk
        )
    )
)


lauk_bp.route(
    "/<int:id_lauk>",
    methods=["DELETE"]
)(
    login_required(
        admin_required(
            delete_lauk
        )
    )
)


lauk_bp.route(
    "/stok/<int:id_lauk>",
    methods=["PUT"]
)(
    login_required(
        admin_required(
            update_stok
        )
    )
)


lauk_bp.route(
    "/status/<int:id_lauk>",
    methods=["PUT"]
)(
    login_required(
        admin_required(
            update_status
        )
    )
)