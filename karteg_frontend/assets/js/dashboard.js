let salesChart = null;
let currentPeriod = "mingguan";

/* =====================================
   HELPER
===================================== */
function formatRupiah(angka) {
    return new Intl.NumberFormat(
        "id-ID",
        {
            style: "currency",
            currency: "IDR",
            minimumFractionDigits: 0
        }
    ).format(angka || 0);
}

/* =====================================
   SUMMARY CARD
===================================== */
async function loadSummary() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard/summary`, { credentials: "include" });
        const result = await response.json();
        if (!result.success) return null;

        const data = result.data;
        const omzetValue = data.total_omzet !== undefined ? data.total_omzet : data.omzet;

        const statPenjualan = document.getElementById("statPenjualan");
        const statTransaksi = document.getElementById("statTransaksi");

        if (statPenjualan) statPenjualan.innerText = formatRupiah(omzetValue || 0);
        if (statTransaksi) statTransaksi.innerText = `${data.total_transaksi || 0} Transaksi`;

        return data;
    } catch (error) {
        console.error("Load Summary Error:", error);
        return null;
    }
}

/* =====================================
   GRAFIK PENJUALAN
===================================== */
async function loadChart(period = "mingguan") {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard/chart?periode=${period}`, { credentials: "include" });
        const result = await response.json();
        if (!result.success) return null;

        const data = result.data;
        renderChart(data);
        return data;
    } catch (error) {
        console.error("Load Chart Error:", error);
        return null;
    }
}

function renderChart(data) {
    const chartEl = document.getElementById("salesChart");
    if (!chartEl) return;
    
    const ctx = chartEl.getContext("2d");
    const labels = data.map(item => item.tanggal);
    const omzet = data.map(item => item.total);

    if (salesChart) {
        salesChart.destroy();
    }

    salesChart = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [
                {
                    label: "Omzet",
                    data: omzet,
                    borderColor: "#3cb531",
                    backgroundColor: "rgba(60,181,49,0.15)",
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

/* =====================================
   MENU TERLARIS
===================================== */
async function loadTopLauk() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard/top-lauk`, { credentials: "include" });
        const result = await response.json();
        if (!result.success) return null;

        renderTopLauk(result.data);
        return result.data;
    } catch (error) {
        console.error("Top Lauk Error:", error);
        return null;
    }
}

function renderTopLauk(data) {
    const container = document.querySelector(".section-card .menu-item");
    if (!container || !data || data.length === 0) return;

    const top = data[0];
    const totalTerjual = top.total !== undefined ? top.total : top.total_terjual;

    container.innerHTML = `
        <div class="menu-rank gold">#1</div>
        <div>
            <div class="menu-name">${top.nama_lauk}</div>
            <div class="menu-price">Total Terjual</div>
        </div>
        <div class="menu-sold">${totalTerjual || 0} Porsi</div>
    `;
}

/* =====================================
   TABEL TOTAL ITEM TERJUAL
===================================== */
async function loadItemTerjual() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard/top-lauk`, { credentials: "include" });
        const result = await response.json();
        if (!result.success) return null;

        renderItemTable(result.data);
        return result.data;
    } catch (error) {
        console.error(error);
        return null;
    }
}

function renderItemTable(data) {
    const tbody = document.querySelector(".custom-table tbody");
    if (!tbody || !data) return;

    tbody.innerHTML = "";
    data.forEach((item, index) => {
        const totalValue = item.total !== undefined ? item.total : item.total_terjual;
        tbody.innerHTML += `
            <tr>
                <td>${index + 1}</td>
                <td class="fw-semibold">${item.nama_lauk}</td>
                <td>
                    <span class="badge text-success-emphasis bg-success-subtle border border-success-subtle rounded-pill px-2">
                        ${item.kategori || "-"}
                    </span>
                </td>
                <td class="text-end fw-bold text-success">${totalValue || 0}</td>
            </tr>
        `;
    });
}

/* =====================================
   STOK HABIS
===================================== */
async function loadStokHabis() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard/stok-habis`, { credentials: "include" });
        const result = await response.json();
        if (!result.success) return [];
        return result.data;
    } catch (error) {
        console.error(error);
        return [];
    }
}

/* =====================================
   INSIGHT BI
===================================== */
async function loadInsight(cachedSummary = null, cachedTopMenu = null, cachedStokHabis = null) {
    try {
        let summary = cachedSummary;
        let topMenu = cachedTopMenu;
        let stokHabis = cachedStokHabis;

        // Ambil data dari server hanya jika data cache tidak dilemparkan oleh fungsi Init
        if (!summary) {
            const response = await fetch(`${API_BASE_URL}/dashboard/summary`, { credentials: "include" });
            const result = await response.json();
            summary = result.data;
        }
        if (!topMenu) {
            const topResponse = await fetch(`${API_BASE_URL}/dashboard/top-lauk`, { credentials: "include" });
            const topResult = await topResponse.json();
            topMenu = topResult.data?.[0];
        }
        if (!stokHabis) {
            stokHabis = await loadStokHabis();
        }

        const insightBox = document.querySelector(".insight-box p");
        if (!insightBox) return;

        const omzetValue = summary?.total_omzet !== undefined ? summary.total_omzet : summary?.omzet;
        const totalTerjual = topMenu?.total !== undefined ? topMenu.total : topMenu?.total_terjual;

        insightBox.innerHTML = `
            Total transaksi saat ini mencapai <b>${summary?.total_transaksi || 0}</b> transaksi dengan omzet sebesar <b>${formatRupiah(omzetValue)}</b>.
            <br><br>
            Produk paling diminati adalah <b>${topMenu?.nama_lauk || "-"}</b> dengan total penjualan <b>${totalTerjual || 0}</b> porsi.
            <br><br>
            Terdapat <b>${stokHabis?.length || 0}</b> item yang stoknya habis dan perlu segera dilakukan restock.
        `;
    } catch (error) {
        console.error("Insight Error:", error);
    }
}

/* =====================================
   PERIODE
===================================== */
function changePeriod(period) {
    currentPeriod = period;
    const label = document.getElementById("periodLabel");
    if (label) {
        label.innerText = period === "mingguan" ? "Mingguan" : "Bulanan";
    }
    loadChart(period);
}

/* =====================================
   INIT (DIOPTIMALKAN DENGAN PROMISE.ALL)
===================================== */
document.addEventListener("DOMContentLoaded", async () => {
    try {
        // Menembak seluruh API secara paralel (bersamaan) untuk menghilangkan lag beruntun
        const [summaryData, chartData, topLaukData, stokHabisData] = await Promise.all([
            loadSummary(),
            loadChart(currentPeriod),
            loadTopLauk(),
            loadStokHabis()
        ]);

        // Merender tabel item terjual menggunakan data top lauk yang sudah diunduh
        if (topLaukData) {
            renderItemTable(topLaukData);
        }

        // Pemuatan Insight langsung menggunakan parameter cache agar terbebas dari duplikasi request
        await loadInsight(summaryData, topLaukData?.[0], stokHabisData);

    } catch (error) {
        console.error("Initialization Dashboard Error:", error);
    }

    // Event Listener Dropdown Periode Grafik
    document.querySelectorAll(".period-option").forEach(option => {
        option.addEventListener("click", () => {
            const value = option.innerText.toLowerCase();
            changePeriod(value);
            const dropdown = document.getElementById("periodDropdown");
            if (dropdown) dropdown.classList.remove("show");
        });
    });
});