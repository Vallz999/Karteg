from flask import Blueprint

from controllers.kategori_controller import (
    get_all_kategori,
    create_kategori,
    update_kategori,
    delete_kategori
)

from middleware.auth_middleware import (
    login_required
)

from middleware.role_middleware import (
    admin_required
)

kategori_bp = Blueprint(
    "kategori",
    __name__
)


kategori_bp.route(
    "/",
    methods=["GET"]
)(
    login_required(
        get_all_kategori
    )
)


kategori_bp.route(
    "/",
    methods=["POST"]
)(
    login_required(
        admin_required(
            create_kategori
        )
    )
)


kategori_bp.route(
    "/<int:id_kategori>",
    methods=["PUT"]
)(
    login_required(
        admin_required(
            update_kategori
        )
    )
)


kategori_bp.route(
    "/<int:id_kategori>",
    methods=["DELETE"]
)(
    login_required(
        admin_required(
            delete_kategori
        )
    )
)