from database.db import fetch_all, fetch_one, execute_query


class TransaksiModel:

    @staticmethod
    def get_all():
        return fetch_all("""
            SELECT *
            FROM transaksi
            ORDER BY tanggal DESC
        """)

    @staticmethod
    def find_by_id(id_transaksi):
        return fetch_one("""
            SELECT *
            FROM transaksi
            WHERE id_transaksi=%s
        """, (
            id_transaksi,
        ))

    @staticmethod
    def create(id_user, total_harga):
        return execute_query("""
            INSERT INTO transaksi
            (id_user,total_harga)
            VALUES (%s,%s)
        """, (
            id_user,
            total_harga
        ))