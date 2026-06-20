function formatRupiah(value) {
    return new Intl.NumberFormat(
        "id-ID",
        {
            style: "currency",
            currency: "IDR",
            minimumFractionDigits: 0
        }
    ).format(value);
}

function formatTanggal(dateString) {

    const date = new Date(dateString);

    return date.toLocaleDateString(
        "id-ID",
        {
            year: "numeric",
            month: "long",
            day: "numeric"
        }
    );
}

function showSuccess(message) {
    alert(message);
}

function showError(message) {
    alert(message);
}

function confirmDelete() {
    return confirm(
        "Yakin ingin menghapus data?"
    );
}

async function logout() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/auth/logout`,
            {
                method: "POST",
                credentials: "include"
            }
        );

        const result = await response.json();

        if (result.status === "success") {
            window.location.href =
                "login.html";
        }

    } catch (error) {
        console.error(error);
    }
}