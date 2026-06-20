USE karteg_db;

-- ====================================================================
-- PRE-SEEDING CLEANUP (Amankan Penjadwalan Ulang Data)
-- ====================================================================
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE detail_pesanan;
TRUNCATE TABLE pesanan;
TRUNCATE TABLE transaksi;
TRUNCATE TABLE lauk;
TRUNCATE TABLE kategori_lauk;
TRUNCATE TABLE user;

SET FOREIGN_KEY_CHECKS = 1;


-- ====================================================================
-- 1. USER DEFAULT
-- ====================================================================
INSERT INTO user (username, password, role)
VALUES
(
    'admin',
    '$2a$12$GSwRAwPPja9r26FQdB4eNuYjiSu/juVgYzQKMqSAbxTE3hU2Wv322',
    'admin'
),
(
    'kasir',
    '$2a$12$uM3d8w6nyUjr9/k7upRTVea79r4yJKZT6.uO5/Nh0DGD8nevFFg76',
    'kasir'
);


-- ====================================================================
-- 2. KATEGORI BARU
-- ====================================================================
INSERT INTO kategori_lauk (id_kategori, nama_kategori)
VALUES
(1, 'Lauk'),
(2, 'Sayur'),
(3, 'Gorengan'),
(4, 'Minuman');


-- ====================================================================
-- 3. DATA LAUK BARU (Sudah Diupdate & Ditambahkan Menu Baru)
-- ====================================================================
INSERT INTO lauk (nama_lauk, harga, stok, status, id_kategori)
VALUES
-- --- KATEGORI: LAUK (id_kategori = 1) ---
('Ayam Goreng', 8000, 20, 'tersedia', 1),
('Telur Balado', 5000, 30, 'tersedia', 1),
('Ikan Lele Goreng', 7000, 15, 'tersedia', 1),
('Sate Jeroan', 3000, 15, 'tersedia', 1),          -- Menggantikan Rendang Daging
('Ayam Geprek', 9000, 15, 'tersedia', 1),           -- Dipertahankan
('Cumi Asin Cabe Ijo', 8500, 12, 'tersedia', 1),
('Perkedel Daging', 4000, 25, 'tersedia', 1),
('Cakalan Suir', 8000, 18, 'tersedia', 1),          -- Menggantikan Ikan Nila Bakar
('Tempe Oreg', 3000, 35, 'tersedia', 1),            -- Menu Baru
('Kentang Mustofa', 4000, 25, 'tersedia', 1),       -- Menu Baru
('Sambal Goreng Kentang', 6000, 20, 'tersedia', 1), -- Menu Baru (Nama diperbaiki)
('Tempe Bacem', 2500, 20, 'tersedia', 1),           -- Menu Baru

-- --- KATEGORI: SAYUR (id_kategori = 2) ---
('Sayur Asem', 3000, 25, 'tersedia', 2),
('Capcay Sayur', 4000, 20, 'tersedia', 2),
('Tumis Kangkung', 3000, 15, 'tersedia', 2),
('Sayur Sop Ayam', 3500, 20, 'tersedia', 2),
('Gulai Daun Singkong', 4000, 15, 'tersedia', 2),
('Tumis Buncis Jagung', 3000, 0, 'habis', 2),

-- --- KATEGORI: GORENGAN (id_kategori = 3) ---
('Tempe Goreng Mendoan', 2000, 50, 'tersedia', 3),
('Tahu Isi Goreng', 2000, 50, 'tersedia', 3),
('Bakwan Sayur', 2000, 40, 'tersedia', 3),
('Cireng Isi Ayam', 2500, 30, 'tersedia', 3),
('Pisang Goreng', 2500, 20, 'tersedia', 3),
('Singkong Goreng Keju', 2000, 0, 'habis', 3),
('Perkedel Kentang', 2500, 30, 'tersedia', 3),      -- Menu Baru

-- --- KATEGORI: MINUMAN (id_kategori = 4) ---
('Es Teh Manis', 3000, 100, 'tersedia', 4),
('Es Jeruk Peras', 4000, 50, 'tersedia', 4),
('Air Mineral Botol', 3000, 80, 'tersedia', 4),
('Teh Tawar Hangat', 1500, 100, 'tersedia', 4);