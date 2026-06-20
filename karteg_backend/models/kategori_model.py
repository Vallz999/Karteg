from database.db import fetch_all, fetch_one, execute_query


class KategoriModel:

    @staticmethod
    def get_all():
        return fetch_all(
            "SELECT * FROM kategori_lauk"
        )

    @staticmethod
    def find_by_id(id_kategori):
        return fetch_one(
            """
            SELECT *
            FROM kategori_lauk
            WHERE id_kategori=%s
            """,
            (id_kategori,)
        )

    @staticmethod
    def create(nama_kategori):
        return execute_query("""
            INSERT INTO kategori_lauk
            (nama_kategori)
            VALUES (%s)
        """, (
            nama_kategori,
        ))

    @staticmethod
    def update(id_kategori, nama_kategori):
        return execute_query("""
            UPDATE kategori_lauk
            SET nama_kategori=%s
            WHERE id_kategori=%s
        """, (
            nama_kategori,
            id_kategori
        ))

    @staticmethod
    def delete(id_kategori):
        return execute_query("""
            DELETE FROM kategori_lauk
            WHERE id_kategori=%s
        """, (
            id_kategori,
        ))