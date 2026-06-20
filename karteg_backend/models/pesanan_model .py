from database.db import (
    fetch_one,
    fetch_all,
    execute_query
)


class PesananModel:

    @staticmethod
    def find_by_id(id_pesanan):
        return fetch_one("""
            SELECT *
            FROM pesanan
            WHERE id_pesanan = %s
        """, (
            id_pesanan,
        ))

    @staticmethod
    def find_by_transaksi(id_transaksi):
        return fetch_one("""
            SELECT *
            FROM pesanan
            WHERE id_transaksi = %s
        """, (
            id_transaksi,
        ))

    @staticmethod
    def create(
        id_transaksi,
        jumlah_nasi,
        harga_nasi
    ):
        return execute_query("""
            INSERT INTO pesanan
            (
                id_transaksi,
                jumlah_nasi,
                harga_nasi
            )
            VALUES (%s,%s,%s)
        """, (
            id_transaksi,
            jumlah_nasi,
            harga_nasi
        ))

    @staticmethod
    def update(
        id_pesanan,
        jumlah_nasi,
        harga_nasi
    ):
        return execute_query("""
            UPDATE pesanan
            SET
                jumlah_nasi = %s,
                harga_nasi = %s
            WHERE id_pesanan = %s
        """, (
            jumlah_nasi,
            harga_nasi,
            id_pesanan
        ))

    @staticmethod
    def delete(id_pesanan):
        return execute_query("""
            DELETE FROM pesanan
            WHERE id_pesanan = %s
        """, (
            id_pesanan,
        ))

    @staticmethod
    def get_total_nasi_terjual():
        return fetch_one("""
            SELECT
                COALESCE(
                    SUM(jumlah_nasi),
                    0
                ) AS total_nasi
            FROM pesanan
        """)

    @staticmethod
    def get_total_pendapatan_nasi():
        return fetch_one("""
            SELECT
                COALESCE(
                    SUM(
                        jumlah_nasi * harga_nasi
                    ),
                    0
                ) AS total_pendapatan_nasi
            FROM pesanan
        """)

    @staticmethod
    def get_default_pesanan():
        """
        Digunakan frontend untuk
        menampilkan nasi default
        pada keranjang transaksi.
        """

        return {
            "nama": "Nasi Putih",
            "jumlah": 1,
            "harga": 5000,
            "subtotal": 5000
        }