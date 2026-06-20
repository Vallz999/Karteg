// ==========================================================================
// STATE & CONFIGURATION GLOBAL
// ==========================================================================
let menuData = [];       // Menyimpan data lauk dari backend
let kategoriMap = {};    // Menyimpan map id_kategori ke nama_kategori
let currentPage = 1;
const perPage = 7;
let filterKat = 'Semua';
let activeIdLauk = null; // Menyimpan ID lauk yang sedang diedit/dihapus

/* ==========================================================================
   ⚡ EAGER FETCHING SYSTEM (Mencuri Start Request API di Background)
   ========================================================================== */
// Jalankan request ke backend secepat mungkin saat file script ini pertama kali dibaca browser
const kategoriPromise = fetch(`${API_BASE_URL}/kategori`, { credentials: "include" })
    .then(res => res.json())
    .catch(err => ({ status: "error", message: err.message }));

const laukPromise = fetch(`${API_BASE_URL}/lauk`, { credentials: "include" })
    .then(res => res.json())
    .catch(err => ({ status: "error", message: err.message }));

// ==========================================================================
// INISIALISASI HALAMAN (DOM CONTENT LOADED - PARALLEL RESOLUTION)
// ==========================================================================
document.addEventListener("DOMContentLoaded", async () => {
    // Tampilkan loading skeleton/spinner pada tabel sesegera mungkin
    showTableLoading();

    try {
        // Selesaikan semua proses data (Kategori & Lauk) secara SIMULTAN tanpa saling memblokir
        const [kategoriResult, laukResult] = await Promise.all([
            kategoriPromise,
            laukPromise
        ]);

        // 1. Proses & Render Opsi Dropdown Kategori
        if (kategoriResult.status === "success" && kategoriResult.data) {
            kategoriResult.data.forEach(kat => {
                kategoriMap[kat.nama_kategori.toLowerCase()] = kat.id_kategori;
            });
            
            const optionsHtml = kategoriResult.data.map(kat => 
                `<option value="${kat.id_kategori}">${kat.nama_kategori}</option>`
            ).join('');
            
            const tambahKatEl = document.getElementById('tambahKategori');
            const editKatEl = document.getElementById('editKategori');
            if (tambahKatEl) tambahKatEl.innerHTML = optionsHtml;
            if (editKatEl) editKatEl.innerHTML = optionsHtml;
        }

        // 2. Proses & Render Data Utama Tabel Lauk
        if (laukResult.status === "success") {
            menuData = laukResult.data || [];
            renderTable();
        } else {
            showToast(laukResult.message || "Gagal mengambil data lauk", "danger");
        }

    } catch (error) {
        console.error("Initialization Error:", error);
        showToast("Gagal menyinkronkan data dari server backend", "danger");
    }

    // 3. Daftarkan Event Listener Elemen UI
    setupEventListeners();
});

// ==========================================
// AMBIL DATA & RENDER
// ==========================================
async function fetchAndRenderData() {
    showTableLoading();
    try {
        const result = await getLauk();
        if (result.status === "success") {
            menuData = result.data || [];
            renderTable();
        } else {
            showToast(result.message || "Gagal mengambil data", "danger");
        }
    } catch (error) {
        console.error(error);
        showToast("Gagal terhubung ke server backend", "danger");
    }
}

function getFiltered() {
    const q = document.getElementById('searchInput').value.toLowerCase();
    return menuData.filter(d => {
        const namaKategori = d.nama_kategori || ''; 
        const matchKat = filterKat === 'Semua' || namaKategori.toLowerCase() === filterKat.toLowerCase();
        const matchQ = d.nama_lauk.toLowerCase().includes(q) || namaKategori.toLowerCase().includes(q);
        return matchKat && matchQ;
    });
}

function renderTable() {
    const data = getFiltered();
    const total = data.length;
    const pages = Math.max(1, Math.ceil(total / perPage));
    if (currentPage > pages) currentPage = pages;

    const slice = data.slice((currentPage - 1) * perPage, currentPage * perPage);
    const tbody = document.getElementById('tableBody');

    if (!tbody) return;

    if (slice.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:40px;color:#aaa;font-size:.9rem">
            <i class="bi bi-inbox" style="font-size:2rem;display:block;margin-bottom:8px"></i>Tidak ada data ditemukan</td></tr>`;
    } else {
        tbody.innerHTML = slice.map(d => {
            const statusLauk = d.status.toLowerCase();
            const badge = statusLauk === 'tersedia'
                ? `<span class="badge-tersedia">Tersedia</span>`
                : `<span class="badge-habis">Habis</span>`;

            return `<tr>
                <td><strong>${d.nama_lauk}</strong></td>
                <td><span style="background:var(--green-pale);color:var(--green-dark);border-radius:20px;padding:3px 10px;font-size:.75rem;font-weight:600">${d.nama_kategori}</span></td>
                <td>${formatRupiah(d.harga)}</td>
                <td>${d.stok}</td>
                <td>${badge}</td>
                <td style="text-align:center">
                    <button class="btn-edit" onclick="openEdit(${d.id_lauk})"><i class="bi bi-pencil-fill"></i> Edit</button>
                    <button class="btn-hapus" onclick="openHapus(${d.id_lauk})"><i class="bi bi-trash-fill"></i> Hapus</button>
                </td>
            </tr>`;
        }).join('');
    }
    renderPagination(pages);
}

function renderPagination(pages) {
    const wrap = document.getElementById('paginationWrap');
    if (!wrap) return;
    let html = `<div class="pg-btn ${currentPage === 1 ? 'disabled' : ''}" onclick="goPage(${currentPage - 1})"><i class="bi bi-chevron-left"></i></div>`;
    for (let i = 1; i <= pages; i++) {
        html += `<div class="pg-btn ${i === currentPage ? 'active' : ''}" onclick="goPage(${i})">${i}</div>`;
    }
    html += `<div class="pg-btn ${currentPage === pages ? 'disabled' : ''}" onclick="goPage(${currentPage + 1})"><i class="bi bi-chevron-right"></i></div>`;
    wrap.innerHTML = html;
}

function goPage(p) {
    currentPage = p;
    renderTable();
}

function showTableLoading() {
    const tbody = document.getElementById('tableBody');
    if (tbody) {
        tbody.innerHTML = `<tr>
            <td colspan="6" style="text-align:center;padding:40px;color:#aaa;font-size:.9rem">
                <i class="bi bi-arrow-clockwise" style="font-size:2rem;display:block;margin-bottom:8px;animation: spin 1s linear infinite;"></i>
                Memuat data terupdate...
            </td>
        </tr>`;
    }
}

// ==========================================
// SETUP LISTENERS & FILTER UI
// ==========================================
function setupEventListeners() {
    // Realtime Search
    document.getElementById('searchInput').addEventListener('input', () => {
        currentPage = 1;
        renderTable();
    });

    // Toggle Dropdown Kategori Atas
    document.getElementById('btnKat').addEventListener('click', (e) => {
        e.stopPropagation();
        document.getElementById('katDropdown').classList.toggle('show');
    });

    // Pilihan Dropdown Kategori Atas
    document.querySelectorAll('#katDropdown .kat-option').forEach(option => {
        option.addEventListener('click', function() {
            filterKat = this.getAttribute('data-value');
            document.getElementById('katDropdown').classList.remove('show');
            document.querySelectorAll('.kat-option').forEach(el => el.classList.remove('selected'));
            this.classList.add('selected');
            currentPage = 1;
            renderTable();
        });
    });

    // Menutup dropdown jika klik di luar area
    document.addEventListener('click', () => {
        const dropdown = document.getElementById('katDropdown');
        if (dropdown) dropdown.classList.remove('show');
    });

    // Tombol Buka Modal Tambah
    document.getElementById('btnTambahBaru').addEventListener('click', openTambah);

    // Tombol Simpan (Submit) Aksi CRUD
    document.getElementById('btnSaveTambah').addEventListener('click', saveTambahHandler);
    document.getElementById('btnSaveEdit').addEventListener('click', saveEditHandler);
    document.getElementById('btnConfirmHapus').addEventListener('click', confirmHapusHandler);

    // Otomatisasi Penutupan Modal via atribut data-close
    document.querySelectorAll('[data-close]').forEach(button => {
        button.addEventListener('click', () => {
            const modalId = button.getAttribute('data-close');
            closeModal(modalId);
        });
    });

    // Klik overlay modal untuk menutup
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) overlay.classList.remove('show');
        });
    });

    // Setup Aksi Logout Sidebar
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            sessionStorage.clear();
            await logout();
        });
    }
}

// Tetap dipertahankan untuk kebutuhan sinkronisasi ulang opsional pasca CRUD
async function loadKategoriOptions() {
    try {
        const res = await getKategori();
        if (res.status === "success" && res.data) {
            res.data.forEach(kat => {
                kategoriMap[kat.nama_kategori.toLowerCase()] = kat.id_kategori;
            });
            const optionsHtml = res.data.map(kat => 
                `<option value="${kat.id_kategori}">${kat.nama_kategori}</option>`
            ).join('');
            document.getElementById('tambahKategori').innerHTML = optionsHtml;
            document.getElementById('editKategori').innerHTML = optionsHtml;
        }
    } catch (err) {
        console.error("Gagal memuat kategori:", err);
    }
}

// ==========================================
// FUNGSI MODAL & LOGIKA CRUD INTEGRATED
// ==========================================
function openModal(id) { document.getElementById(id).classList.add('show'); }
function closeModal(id) { document.getElementById(id).classList.remove('show'); }

// --- TAMBAH DATA ---
function openTambah() {
    document.getElementById('tambahNama').value = '';
    document.getElementById('tambahHarga').value = '';
    document.getElementById('tambahStok').value = '';
    openModal('modalTambah');
}

async function saveTambahHandler() {
    const nama_lauk = document.getElementById('tambahNama').value.trim();
    const harga = parseInt(document.getElementById('tambahHarga').value);
    const stok = parseInt(document.getElementById('tambahStok').value);
    const id_kategori = parseInt(document.getElementById('tambahKategori').value);
    const status = document.getElementById('tambahStatus').value.toLowerCase();

    if (!nama_lauk) return showToast('Nama menu tidak boleh kosong!', 'danger');
    if (isNaN(harga) || isNaN(stok)) return showToast('Harga dan Stok harus diisi angka valid!', 'danger');

    const payload = { nama_lauk, harga, stok, status, id_kategori };
    
    const result = await tambahLauk(payload);
    if (result.status === "success") {
        closeModal('modalTambah');
        showToast(`"${nama_lauk}" berhasil ditambahkan`, 'success');
        await fetchAndRenderData();
    } else {
        showToast(result.message || "Gagal menambah data", "danger");
    }
}

// --- EDIT DATA ---
function openEdit(idLauk) {
    activeIdLauk = idLauk;
    const target = menuData.find(item => item.id_lauk === idLauk);
    if (!target) return;

    document.getElementById('editNama').value = target.nama_lauk;
    document.getElementById('editHarga').value = target.harga;
    document.getElementById('editStok').value = target.stok;
    document.getElementById('editKategori').value = target.id_kategori;
    
    const options = Array.from(document.getElementById('editStatus').options).map(o => o.value);
    const matchStatus = options.find(o => o.toLowerCase() === target.status.toLowerCase()) || options[0];
    document.getElementById('editStatus').value = matchStatus;

    openModal('modalEdit');
}

async function saveEditHandler() {
    const nama_lauk = document.getElementById('editNama').value.trim();
    const harga = parseInt(document.getElementById('editHarga').value);
    const stok = parseInt(document.getElementById('editStok').value);
    const id_kategori = parseInt(document.getElementById('editKategori').value);
    const status = document.getElementById('editStatus').value.toLowerCase();

    if (!nama_lauk) return showToast('Nama menu tidak boleh kosong!', 'danger');

    const payload = { nama_lauk, harga, stok, status, id_kategori };

    const result = await updateLauk(activeIdLauk, payload);
    if (result.status === "success") {
        closeModal('modalEdit');
        showToast(`"${nama_lauk}" berhasil diperbarui`, 'success');
        await fetchAndRenderData();
    } else {
        showToast(result.message || "Gagal mengupdate data", "danger");
    }
}

// --- HAPUS DATA ---
function openHapus(idLauk) {
    activeIdLauk = idLauk;
    const target = menuData.find(item => item.id_lauk === idLauk);
    if (!target) return;
    
    document.getElementById('hapusNama').textContent = `"${target.nama_lauk}"`;
    openModal('modalHapus');
}

async function confirmHapusHandler() {
    const result = await hapusLauk(activeIdLauk);
    if (result && result.status === "success") {
        closeModal('modalHapus');
        showToast("Data berhasil dihapus secara permanen", "danger");
        await fetchAndRenderData();
    } else if (result) {
        showToast(result.message || "Gagal menghapus data", "danger");
    }
}

// ==========================================
// TOAST NOTIFICATION UI INTERACTIVE
// ==========================================
function showToast(msg, type = 'success') {
    const wrap = document.getElementById('toastWrap');
    if (!wrap) return;
    const icon = type === 'success' ? 'bi-check-circle-fill' : 'bi-x-circle-fill';
    const el = document.createElement('div');
    el.className = `toast-item ${type}`;
    el.innerHTML = `<i class="bi ${icon}"></i> ${msg}`;
    wrap.appendChild(el);
    setTimeout(() => el.remove(), 3000);
}

/* ==========================================================================
   KODE FUNGSI FETCH BAWAAN USER (TETAP DIPERTAHANKAN SEUTUHNYA)
   ========================================================================== */

/* =====================
   KATEGORI
===================== */
async function getKategori() {
    const response = await fetch(`${API_BASE_URL}/kategori`, { credentials: "include" });
    return await response.json();
}

async function tambahKategori(nama_kategori) {
    const response = await fetch(`${API_BASE_URL}/kategori`, {
        method: "POST",
        ...FETCH_CONFIG,
        body: JSON.stringify({ nama_kategori })
    });
    return await response.json();
}

async function updateKategori(id, nama_kategori) {
    const response = await fetch(`${API_BASE_URL}/kategori/${id}`, {
        method: "PUT",
        ...FETCH_CONFIG,
        body: JSON.stringify({ nama_kategori })
    });
    return await response.json();
}

async function hapusKategori(id) {
    if (!confirmDelete()) return;
    const response = await fetch(`${API_BASE_URL}/kategori/${id}`, { method: "DELETE", credentials: "include" });
    return await response.json();
}

/* =====================
   LAUK
===================== */
async function getLauk() {
    const response = await fetch(`${API_BASE_URL}/lauk`, { credentials: "include" });
    return await response.json();
}

async function tambahLauk(data) {
    const response = await fetch(`${API_BASE_URL}/lauk`, {
        method: "POST",
        ...FETCH_CONFIG,
        body: JSON.stringify(data)
    });
    return await response.json();
}

async function updateLauk(id, data) {
    const response = await fetch(`${API_BASE_URL}/lauk/${id}`, {
        method: "PUT",
        ...FETCH_CONFIG,
        body: JSON.stringify(data)
    });
    return await response.json();
}

async function hapusLauk(id) {
    if (!confirmDelete()) return;
    const response = await fetch(`${API_BASE_URL}/lauk/${id}`, { method: "DELETE", credentials: "include" });
    return await response.json();
}

async function updateStok(id, stok) {
    const response = await fetch(`${API_BASE_URL}/lauk/stok/${id}`, {
        method: "PUT",
        ...FETCH_CONFIG,
        body: JSON.stringify({ stok })
    });
    return await response.json();
}

async function updateStatus(id, status) {
    const response = await fetch(`${API_BASE_URL}/lauk/status/${id}`, {
        method: "PUT",
        ...FETCH_CONFIG,
        body: JSON.stringify({ status })
    });
    return await response.json();
}