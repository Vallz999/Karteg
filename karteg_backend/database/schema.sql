CREATE DATABASE IF NOT EXISTS karteg_db;
USE karteg_db;


-- =========================
-- USER
-- =========================
CREATE TABLE user (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'kasir') NOT NULL
);


-- =========================
-- KATEGORI LAUK
-- =========================
CREATE TABLE kategori_lauk (
    id_kategori INT AUTO_INCREMENT PRIMARY KEY,
    nama_kategori VARCHAR(100) NOT NULL
);


-- =========================
-- LAUK
-- =========================
CREATE TABLE lauk (
    id_lauk INT AUTO_INCREMENT PRIMARY KEY,
    nama_lauk VARCHAR(100) NOT NULL,
    harga INT NOT NULL,
    stok INT NOT NULL DEFAULT 0,
    status ENUM('tersedia', 'habis') DEFAULT 'tersedia',
    id_kategori INT,

    FOREIGN KEY (id_kategori)
        REFERENCES kategori_lauk(id_kategori)
        ON DELETE CASCADE
);


-- =========================
-- TRANSAKSI
-- =========================
CREATE TABLE transaksi (
    id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_harga INT NOT NULL,

    FOREIGN KEY (id_user)
        REFERENCES user(id_user)
        ON DELETE CASCADE
);


-- =========================
-- PESANAN
-- =========================
CREATE TABLE pesanan (
    id_pesanan INT AUTO_INCREMENT PRIMARY KEY,
    id_transaksi INT NOT NULL,
    jumlah_nasi INT NOT NULL,
    harga_nasi INT NOT NULL,

    FOREIGN KEY (id_transaksi)
        REFERENCES transaksi(id_transaksi)
        ON DELETE CASCADE
);


-- =========================
-- DETAIL PESANAN
-- =========================
CREATE TABLE detail_pesanan (
    id_detail INT AUTO_INCREMENT PRIMARY KEY,
    id_pesanan INT NOT NULL,
    id_lauk INT NOT NULL,
    qty INT NOT NULL,
    subtotal INT NOT NULL,

    FOREIGN KEY (id_pesanan)
        REFERENCES pesanan(id_pesanan)
        ON DELETE CASCADE,

    FOREIGN KEY (id_lauk)
        REFERENCES lauk(id_lauk)
        ON DELETE CASCADE
);