def validate_login(data):
    errors = []

    if not data.get("username"):
        errors.append("Username wajib diisi")

    if not data.get("password"):
        errors.append("Password wajib diisi")

    return errors


def validate_kategori(data):
    errors = []

    if not data.get("nama_kategori"):
        errors.append("Nama kategori wajib diisi")

    return errors


def validate_lauk(data):
    errors = []

    if not data.get("nama_lauk"):
        errors.append("Nama lauk wajib diisi")

    if not data.get("harga"):
        errors.append("Harga wajib diisi")

    if data.get("stok") is None:
        errors.append("Stok wajib diisi")

    if not data.get("status"):
        errors.append("Status wajib diisi")

    if not data.get("id_kategori"):
        errors.append("Kategori wajib dipilih")

    return errors


def validate_transaksi(data):
    errors = []

    if not data.get("jumlah_nasi"):
        errors.append("Jumlah nasi wajib diisi")

    if not data.get("harga_nasi"):
        errors.append("Harga nasi wajib diisi")

    if not data.get("items"):
        errors.append("Minimal satu lauk harus dipilih")

    if not data.get("total_harga"):
        errors.append("Total transaksi wajib ada")

    return errors


def validate_date_filter(start, end):
    errors = []

    if not start:
        errors.append("Tanggal awal wajib diisi")

    if not end:
        errors.append("Tanggal akhir wajib diisi")

    return errors