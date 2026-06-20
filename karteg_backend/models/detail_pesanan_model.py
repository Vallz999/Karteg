from database.db import fetch_all, execute_query


class DetailPesananModel:

    @staticmethod
    def get_by_transaksi(id_transaksi):
        return fetch_all("""
            SELECT
                l.nama_lauk,
                dp.qty,
                dp.subtotal
            FROM detail_pesanan dp
            JOIN lauk l
            ON dp.id_lauk=l.id_lauk
            JOIN pesanan p
            ON dp.id_pesanan=p.id_pesanan
            WHERE p.id_transaksi=%s
        """, (
            id_transaksi,
        ))

    @staticmethod
    def create(
        id_pesanan,
        id_lauk,
        qty,
        subtotal
    ):
        return execute_query("""
            INSERT INTO detail_pesanan
            (id_pesanan,id_lauk,qty,subtotal)
            VALUES (%s,%s,%s,%s)
        """, (
            id_pesanan,
            id_lauk,
            qty,
            subtotal
        ))