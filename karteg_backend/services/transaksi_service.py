from database.db import get_connection
from services.stok_service import stok_tersedia


# ==========================================
# KONFIGURASI DEFAULT KARTEG
# ==========================================

DEFAULT_NASI = {
    "nama": "Nasi Putih",
    "harga": 5000,
    "jumlah": 1
}


# ==========================================
# DEFAULT PESANAN
# Digunakan saat halaman transaksi dibuka
# ==========================================

def get_default_pesanan():

    return {
        "nama": DEFAULT_NASI["nama"],
        "harga": DEFAULT_NASI["harga"],
        "jumlah": DEFAULT_NASI["jumlah"],
        "subtotal": (
            DEFAULT_NASI["harga"]
            * DEFAULT_NASI["jumlah"]
        )
    }


# ==========================================
# MEMBUAT TRANSAKSI BARU
# ==========================================

def create_transaction(user_id, data):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ==============================
        # Validasi stok seluruh lauk
        # ==============================

        for item in data["items"]:

            if not stok_tersedia(
                item["id_lauk"],
                item["qty"]
            ):
                raise Exception(
                    f"Stok lauk ID {item['id_lauk']} tidak cukup"
                )

        # ==============================
        # Default nasi
        # Jika frontend tidak mengirim
        # maka gunakan default sistem
        # ==============================

        jumlah_nasi = data.get(
            "jumlah_nasi",
            DEFAULT_NASI["jumlah"]
        )

        harga_nasi = data.get(
            "harga_nasi",
            DEFAULT_NASI["harga"]
        )

        # ==============================
        # Hitung total ulang dari backend
        # agar lebih aman
        # ==============================

        total_harga = (
            jumlah_nasi * harga_nasi
        )

        for item in data["items"]:
            total_harga += item["subtotal"]

        # ==============================
        # Simpan transaksi
        # ==============================

        cursor.execute("""
            INSERT INTO transaksi
            (
                id_user,
                total_harga
            )
            VALUES (%s,%s)
        """, (
            user_id,
            total_harga
        ))

        transaksi_id = cursor.lastrowid

        # ==============================
        # Simpan pesanan (nasi)
        # ==============================

        cursor.execute("""
            INSERT INTO pesanan
            (
                id_transaksi,
                jumlah_nasi,
                harga_nasi
            )
            VALUES (%s,%s,%s)
        """, (
            transaksi_id,
            jumlah_nasi,
            harga_nasi
        ))

        pesanan_id = cursor.lastrowid

        # ==============================
        # Simpan detail lauk
        # ==============================

        for item in data["items"]:

            cursor.execute("""
                INSERT INTO detail_pesanan
                (
                    id_pesanan,
                    id_lauk,
                    qty,
                    subtotal
                )
                VALUES (%s,%s,%s,%s)
            """, (
                pesanan_id,
                item["id_lauk"],
                item["qty"],
                item["subtotal"]
            ))

            # ==========================
            # Kurangi stok lauk
            # ==========================

            cursor.execute("""
                UPDATE lauk
                SET stok = stok - %s
                WHERE id_lauk = %s
            """, (
                item["qty"],
                item["id_lauk"]
            ))

        conn.commit()

        return {
            "status": True,
            "message": "Transaksi berhasil disimpan",
            "transaksi_id": transaksi_id,
            "total_harga": total_harga,
            "jumlah_nasi": jumlah_nasi,
            "harga_nasi": harga_nasi
        }

    except Exception as e:

        conn.rollback()

        return {
            "status": False,
            "message": str(e)
        }

    finally:

        cursor.close()
        conn.close()