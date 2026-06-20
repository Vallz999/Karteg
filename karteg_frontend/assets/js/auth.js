// ==========================================================================
// KARTEG - AUTH.JS (VERSI TERPADU, ANTI-FLASH, ANTI-LOOP & SESSION BASED)
// ==========================================================================

(function () {
    // Ambil rute URL dan data sesi secara INSTAN (Synchronous) di awal pemuatan skrip
    const currentUrl = window.location.pathname;
    const isRootOrIndex = currentUrl === "/" || currentUrl.endsWith("index.html") || currentUrl.endsWith("/");
    const isLoginPage = currentUrl.includes("login.html");

    // Menggunakan sessionStorage sesuai standar keamanan terdistribusi KarTeg
    const isLoggedIn = sessionStorage.getItem("isLoggedIn");
    const role = sessionStorage.getItem("role");

    // ====================================================================
    // 1. BYPASS & ROUTING INSTAN UNTUK HALAMAN LOGIN DAN ROOT (INDEX)
    // ====================================================================
    if (isLoginPage || isRootOrIndex) {
        // Jika user SUDAH login tapi tersesat ke root (/) atau login.html, langsung alihkan
        if (isLoggedIn === "true" && role) {
            if (role === "admin") {
                window.location.href = "/pages/dashboard_admin.html";
            } else {
                window.location.href = "/pages/dashboard_transaksi_kasir.html";
            }
            return; 
        }

        // Jika user BELUM login dan berada di root (/), tendang instan ke halaman login
        if (isRootOrIndex) {
            window.location.href = "/pages/login.html";
            return;
        }

        return; // Biarkan user tetap di halaman login jika memang belum terautentikasi
    }

    // ====================================================================
    // 2. PROTEKSI INSTAN UNTUK HALAMAN DASHBOARD / RIWAYAT / KELOLA DATA
    // ====================================================================
    
    // Validasi Awal: Jika data lokal kosong, tendang langsung ke login sebelum halaman sempat merender UI
    if (isLoggedIn !== "true" || !role) {
        console.warn("Akses ditolak: Sesi lokal tidak ditemukan.");
        sessionStorage.clear();
        window.location.href = "/pages/login.html";
        return; 
    }

    // 3. PROTEKSI PERSILANGAN HAK AKSES LOKAL (ROLE ACCESS GUARD)
    // Cegah Kasir masuk ke area Admin
    if (currentUrl.includes("dashboard_admin.html") && role !== "admin") {
        console.warn("Akses ditolak: Halaman ini khusus Admin!");
        window.location.href = "/pages/login.html";
        return;
    }
    
    // Cegah Admin masuk ke area Kasir
    if (currentUrl.includes("dashboard_transaksi_kasir.html") && role !== "kasir") {
        console.warn("Akses ditolak: Halaman ini khusus Kasir!");
        window.location.href = "/pages/login.html";
        return;
    }

    // ====================================================================
    // 4. VALIDASI KEASLIAN SESSION DI BACKGROUND (SILENT VERIFICATION)
    // ====================================================================
    // Langkah ini berjalan di latar belakang secara async agar perpindahan halaman mulus bebas lag
    async function verifyBackendSession() {
        // Fallback aman jika script config.js termuat sedikit terlambat
        const baseUrl = typeof API_BASE_URL !== 'undefined' ? API_BASE_URL : "http://localhost:5000/api";
        
        try {
            const response = await fetch(`${baseUrl}/auth/session`, {
                method: "GET",
                credentials: "include" // Wajib mengirimkan cookie session aktif milik Flask
            });

            // Jika Flask merespon selain 200 (misal 401 Unauthorized), berarti sesi server mati / dirusak
            if (response.status !== 200) {
                console.warn("Sesi di server backend telah kedaluwarsa atau tidak valid.");
                sessionStorage.clear();
                window.location.href = "/pages/login.html";
            } else {
                const result = await response.json();
                console.log("Sesi Terverifikasi Server. Terautentikasi sebagai:", result.data.role);
            }

        } catch (error) {
            console.error("Gagal sinkronisasi sesi ke backend:", error);
            // Mode Toleransi Kendala Jaringan: Jika server offline/dev error, 
            // biarkan tetap masuk menggunakan basis data sessionStorage lokal yang sudah lolos uji di atas
        }
    }

    // Eksekusi verifikasi server secara aman setelah atau selama siklus render berjalan
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", verifyBackendSession);
    } else {
        verifyBackendSession();
    }
})();