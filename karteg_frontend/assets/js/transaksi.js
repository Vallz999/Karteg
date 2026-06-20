let cart = [];

async function loadLaukTersedia() {

    const response = await fetch(
        `${API_BASE_URL}/transaksi/lauk`,
        {
            credentials: "include"
        }
    );

    const result = await response.json();

    return result.data;
}


function addToCart(
    id_lauk,
    nama_lauk,
    harga
) {

    const existing =
        cart.find(
            item =>
                item.id_lauk === id_lauk
        );

    if (existing) {

        existing.qty += 1;

        existing.subtotal =
            existing.qty * harga;

    } else {

        cart.push({
            id_lauk,
            nama_lauk,
            harga,
            qty: 1,
            subtotal: harga
        });
    }

    renderCart();
}


function renderCart() {

    let total = 0;

    cart.forEach(item => {
        total += item.subtotal;
    });

    const jumlahNasi =
        parseInt(
            document.getElementById(
                "jumlahNasi"
            ).value || 0
        );

    total += jumlahNasi * 5000;

    document.getElementById(
        "totalHarga"
    ).innerText =
        formatRupiah(total);
}


async function simpanTransaksi() {

    const jumlahNasi =
        parseInt(
            document.getElementById(
                "jumlahNasi"
            ).value
        );

    const hargaNasi = 5000;

    const totalHarga =
        cart.reduce(
            (sum, item) =>
                sum + item.subtotal,
            0
        ) +
        (jumlahNasi * hargaNasi);

    const response = await fetch(
        `${API_BASE_URL}/transaksi`,
        {
            method: "POST",
            ...FETCH_CONFIG,
            body: JSON.stringify({
                jumlah_nasi: jumlahNasi,
                harga_nasi: hargaNasi,
                total_harga: totalHarga,
                items: cart
            })
        }
    );

    const result =
        await response.json();

    if (result.status === "success") {

        showSuccess(
            result.message
        );

        cart = [];

    } else {

        showError(
            result.message
        );
    }
}