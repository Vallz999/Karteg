from database.db import fetch_all, fetch_one, execute_query


class LaukModel:

    @staticmethod
    def get_all():
        return fetch_all("""
            SELECT l.*, k.nama_kategori
            FROM lauk l
            JOIN kategori_lauk k
            ON l.id_kategori=k.id_kategori
        """)

    @staticmethod
    def get_available():
        return fetch_all("""
            SELECT *
            FROM lauk
            WHERE stok > 0
            AND status='tersedia'
        """)

    @staticmethod
    def find_by_id(id_lauk):
        return fetch_one("""
            SELECT *
            FROM lauk
            WHERE id_lauk=%s
        """, (id_lauk,))

    @staticmethod
    def create(
        nama_lauk,
        harga,
        stok,
        status,
        id_kategori
    ):
        return execute_query("""
            INSERT INTO lauk
            (nama_lauk,harga,stok,status,id_kategori)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            nama_lauk,
            harga,
            stok,
            status,
            id_kategori
        ))

    @staticmethod
    def update(
        id_lauk,
        nama_lauk,
        harga,
        stok,
        status,
        id_kategori
    ):
        return execute_query("""
            UPDATE lauk
            SET nama_lauk=%s,
                harga=%s,
                stok=%s,
                status=%s,
                id_kategori=%s
            WHERE id_lauk=%s
        """, (
            nama_lauk,
            harga,
            stok,
            status,
            id_kategori,
            id_lauk
        ))

    @staticmethod
    def delete(id_lauk):
        return execute_query("""
            DELETE FROM lauk
            WHERE id_lauk=%s
        """, (id_lauk,))

    @staticmethod
    def update_stok(id_lauk, stok):
        return execute_query("""
            UPDATE lauk
            SET stok=%s
            WHERE id_lauk=%s
        """, (
            stok,
            id_lauk
        ))

    @staticmethod
    def update_status(id_lauk, status):
        return execute_query("""
            UPDATE lauk
            SET status=%s
            WHERE id_lauk=%s
        """, (
            status,
            id_lauk
        ))