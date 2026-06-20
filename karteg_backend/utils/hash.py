import bcrypt


def hash_password(password):
    """
    Hash password sebelum disimpan ke database
    """

    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, hashed_password):
    """
    Verifikasi password login
    """

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
