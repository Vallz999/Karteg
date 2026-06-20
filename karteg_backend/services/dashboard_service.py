from database.db import fetch_one, fetch_all


def summary_data():
    """
    Ringkasan data dashboard - Dioptimalkan dengan meminimalkan trip database
    """
    # Menggabungkan pencarian transaksi dasar ke dalam 1 query tunggal
    transaksi_stats = fetch_one(
        """
        SELECT 
            COUNT(*) AS total_transaksi,
            COALESCE(SUM(total_harga), 0) AS omzet
        FROM transaksi
        """
    )

    stok_habis_count = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM lauk
        WHERE stok <= 0
        """
    )

    return {
        "total_transaksi": transaksi_stats["total_transaksi"],
        "omzet": transaksi_stats["omzet"],
        "total_omzet": transaksi_stats["omzet"],  # Menyelesaikan mismatch properti di frontend
        "stok_habis": stok_habis_count["total"]
    }


def chart_penjualan():
    """
    Grafik omzet per hari
    """
    return fetch_all(
        """
        SELECT
            DATE(tanggal) AS tanggal,
            SUM(total_harga) AS total
        FROM transaksi
        GROUP BY DATE(tanggal)
        ORDER BY tanggal ASC
        """
    )


def top_lauk():
    """
    5 lauk terlaris - Menambahkan alias 'total' agar pas dengan frontend
    """
    return fetch_all(
        """
        SELECT
            l.id_lauk,
            l.nama_lauk,
            SUM(dp.qty) AS total,
            SUM(dp.qty) AS total_terjual
        FROM detail_pesanan dp
        JOIN lauk l
            ON dp.id_lauk = l.id_lauk
        GROUP BY
            l.id_lauk,
            l.nama_lauk
        ORDER BY total DESC
        LIMIT 5
        """
    )


def stok_habis():
    """
    Lauk dengan stok habis
    """
    return fetch_all(
        """
        SELECT
            id_lauk,
            nama_lauk,
            stok
        FROM lauk
        WHERE stok <= 0
        ORDER BY nama_lauk
        """
    )


def omzet_hari_ini():
    """
    Omzet hari ini
    """
    result = fetch_one(
        """
        SELECT
            COALESCE(
                SUM(total_harga),
                0
            ) AS total
        FROM transaksi
        WHERE DATE(tanggal) = CURDATE()
        """
    )
    return result["total"]


def total_nasi_terjual():
    """
    Total nasi yang telah terjual
    """
    result = fetch_one(
        """
        SELECT
            COALESCE(
                SUM(jumlah_nasi),
                0
            ) AS total
        FROM pesanan
        """
    )
    return result["total"]


def total_item_terjual():
    """
    Total seluruh lauk/minuman/sayur yang terjual
    """
    result = fetch_one(
        """
        SELECT
            COALESCE(
                SUM(qty),
                0
            ) AS total
        FROM detail_pesanan
        """
    )
    return result["total"]


def penjualan_per_kategori():
    """
    BI tambahan: Total penjualan berdasarkan kategori
    """
    return fetch_all(
        """
        SELECT
            k.nama_kategori,
            COALESCE(
                SUM(dp.qty),
                0
            ) AS total_terjual
        FROM detail_pesanan dp
        JOIN lauk l
            ON dp.id_lauk = l.id_lauk
        JOIN kategori k
            ON l.id_kategori = k.id_kategori
        GROUP BY
            k.id_kategori,
            k.nama_kategori
        ORDER BY total_terjual DESC
        """
    )


def omzet_per_kategori():
    """
    BI tambahan: Omzet berdasarkan kategori
    """
    return fetch_all(
        """
        SELECT
            k.nama_kategori,
            COALESCE(
                SUM(
                    dp.qty * dp.harga_satuan
                ),
                0
            ) AS omzet
        FROM detail_pesanan dp
        JOIN lauk l
            ON dp.id_lauk = l.id_lauk
        JOIN kategori k
            ON l.id_kategori = k.id_kategori
        GROUP BY
            k.id_kategori,
            k.nama_kategori
        ORDER BY omzet DESC
        """
    )