from database.db import execute_query, fetch_one


def reduce_stok(id_lauk, qty):
    execute_query("""
        UPDATE lauk
        SET stok = stok - %s
        WHERE id_lauk=%s
    """, (
        qty,
        id_lauk
    ))

    update_status(id_lauk)


def add_stok(id_lauk, qty):
    execute_query("""
        UPDATE lauk
        SET stok = stok + %s
        WHERE id_lauk=%s
    """, (
        qty,
        id_lauk
    ))

    update_status(id_lauk)


def update_status(id_lauk):
    lauk = fetch_one("""
        SELECT stok
        FROM lauk
        WHERE id_lauk=%s
    """, (id_lauk,))

    if not lauk:
        return

    status = "tersedia"

    if lauk["stok"] <= 0:
        status = "habis"

    execute_query("""
        UPDATE lauk
        SET status=%s
        WHERE id_lauk=%s
    """, (
        status,
        id_lauk
    ))


def stok_tersedia(id_lauk, qty):
    lauk = fetch_one("""
        SELECT stok
        FROM lauk
        WHERE id_lauk=%s
    """, (id_lauk,))

    if not lauk:
        return False

    return lauk["stok"] >= qty