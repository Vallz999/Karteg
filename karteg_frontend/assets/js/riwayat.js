// ======================================
// RIWAYAT.JS (FINAL - FIX PATH)
// ======================================

document.addEventListener("DOMContentLoaded", async () => {
    try {
        if (typeof checkSession === "function") {
            await checkSession(); 
        }
        setupRoleUI();
        await loadRiwayatTable();
    } catch (error) {
        console.error(error);
        alert("Gagal memuat data riwayat");
    }
});

function setupRoleUI() {
    const role = localStorage.getItem("role");
    const dashboardLink = document.getElementById("dashboardLink");

    if (!dashboardLink) return;

    // Menuju ke file sesama folder pages/
    if (role === "admin") {
        dashboardLink.href = "dashboard_admin.html";
    } else {
        dashboardLink.href = "dashboard_transaksi_kasir.html";
    }
}

async function loadRiwayat() {
    try {
        const response = await fetch(`${API_BASE_URL}/riwayat`, {
            method: "GET",
            ...FETCH_CONFIG,
            headers: {
                ...FETCH_CONFIG.headers,
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        });
        
        if (response.status === 401) {
            alert("Sesi Anda habis, harap login kembali.");
            localStorage.clear();
            window.location.href = "login.html";
            return [];
        }

        const result = await response.json();
        return result.data || [];
    } catch (error) {
        console.error("Error Load Riwayat:", error);
        return [];
    }
}

async function detailRiwayat(id_transaksi) {
    try {
        const response = await fetch(`${API_BASE_URL}/riwayat/${id_transaksi}`, {
            method: "GET",
            ...FETCH_CONFIG,
            headers: {
                ...FETCH_CONFIG.headers,
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        });
        const result = await response.json();
        return result.data;
    } catch (error) {
        console.error("Error Detail Riwayat:", error);
        return null;
    }
}

async function filterRiwayat() {
    try {
        const start = document.getElementById("startDate").value;
        const end = document.getElementById("endDate").value;

        if (!start || !end) {
            alert("Harap isi rentang kedua tanggal filter!");
            return null;
        }

        const response = await fetch(`${API_BASE_URL}/riwayat/filter?start=${start}&end=${end}`, {
            method: "GET",
            ...FETCH_CONFIG,
            headers: {
                ...FETCH_CONFIG.headers,
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        });
        const result = await response.json();
        return result.data || [];
    } catch (error) {
        console.error("Error Filter Riwayat:", error);
        return [];
    }
}

async function loadRiwayatTable() {
    document.getElementById("startDate").value = "";
    document.getElementById("endDate").value = "";
    
    const data = await loadRiwayat();
    renderRiwayatTable(data);
}

async function applyFilter() {
    const data = await filterRiwayat();
    if (data) {
        renderRiwayatTable(data);
    }
}

function renderRiwayatTable(data) {
    const tbody = document.getElementById("riwayatTableBody");
    const statTrx = document.getElementById("statTrx");
    const statPend = document.getElementById("statPend");

    if (!tbody) return;
    tbody.innerHTML = "";

    let totalPendapatan = 0;
    if (statTrx) statTrx.textContent = data.length;

    if (!data || !data.length) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted py-4">
                    <i class="bi bi-inbox d-block fs-3 mb-2"></i> Tidak ada data transaksi ditemukan
                </td>
            </tr>
        `;
        if (statPend) statPend.textContent = typeof formatRupiah === "function" ? formatRupiah(0) : "Rp 0";
        return;
    }

    data.forEach((item, index) => {
        totalPendapatan += Number(item.total_harga || 0);

        const tglFormatted = typeof formatTanggal === "function" ? formatTanggal(item.tanggal) : item.tanggal;
        const hargaFormatted = typeof formatRupiah === "function" ? formatRupiah(item.total_harga) : `Rp ${item.total_harga}`;

        tbody.innerHTML += `
            <tr>
                <td><strong>${index + 1}</strong></td>
                <td><span class="badge bg-light text-dark border">#${item.id_transaksi}</span></td>
                <td>${tglFormatted}</td>
                <td>${item.total_item || 0} Porsi</td>
                <td><strong class="text-success">${hargaFormatted}</strong></td>
                <td style="text-align:center">
                    <button class="btn btn-sm btn-success" onclick="showDetail(${item.id_transaksi})" style="background:var(--green-main); border:none; border-radius:8px; padding: 5px 14px;">
                        <i class="bi bi-eye-fill me-1"></i> Detail
                    </button>
                </td>
            </tr>
        `;
    });

    if (statPend) statPend.textContent = typeof formatRupiah === "function" ? formatRupiah(totalPendapatan) : `Rp ${totalPendapatan}`;
}

async function showDetail(id_transaksi) {
    const data = await detailRiwayat(id_transaksi);

    if (!data || !data.detail) {
        alert("Detail transaksi tidak ditemukan / kosong.");
        return;
    }

    const detailBody = document.getElementById("detailBody");
    if (!detailBody) return;

    let html = "";
    data.detail.forEach(item => {
        const namaLauk = item.nama_lauk || item.nama || "Menu";
        const subtotalItem = item.subtotal || (item.harga * item.qty);
        
        const hargaItemFormatted = typeof formatRupiah === "function" ? formatRupiah(item.harga) : `Rp ${item.harga}`;
        const subtotalFormatted = typeof formatRupiah === "function" ? formatRupiah(subtotalItem) : `Rp ${subtotalItem}`;

        html += `
            <tr class="border-bottom" style="border-color: #f0f7ef !important;">
                <td><strong>${namaLauk}</strong></td>
                <td>${item.qty}x</td>
                <td class="text-muted">${hargaItemFormatted}</td>
                <td><strong class="text-dark">${subtotalFormatted}</strong></td>
            </tr>
        `;
    });

    detailBody.innerHTML = html;

    const modalElement = document.getElementById("detailModal");
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}