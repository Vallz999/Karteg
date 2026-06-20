from flask import Blueprint

from controllers.auth_controller import (
    login,
    register,
    logout,
    check_session
)

from middleware.auth_middleware import (
    login_required
)

auth_bp = Blueprint(
    "auth",
    __name__
)


auth_bp.route(
    "/login",
    methods=["POST"]
)(login)


auth_bp.route(
    "/logout",
    methods=["POST"]
)(
    login_required(logout)
)


auth_bp.route(
    "/session",
    methods=["GET"]
)(
    login_required(check_session)
)

from middleware.role_middleware import (
    admin_required
)

auth_bp.route(
    "/register",
    methods=["POST"]
)(
    login_required(
        admin_required(
            register
        )
    )
)