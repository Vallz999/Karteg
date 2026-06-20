from services.dashboard_service import (
    summary_data,
    chart_penjualan,
    top_lauk,
    stok_habis,
    omzet_hari_ini,
    total_nasi_terjual,
    total_item_terjual
)

from utils.helper import success_response


def get_summary():
    """
    Ringkasan dashboard BI
    """

    data = summary_data()

    data["omzet_hari_ini"] = omzet_hari_ini()
    data["total_nasi_terjual"] = total_nasi_terjual()
    data["total_item_terjual"] = total_item_terjual()

    return success_response(
        data=data
    )


def get_penjualan_chart():
    """
    Data grafik penjualan
    """

    return success_response(
        data=chart_penjualan()
    )


def get_lauk_terlaris():
    """
    Top produk terlaris
    """

    return success_response(
        data=top_lauk()
    )


def get_stok_habis():
    """
    Produk stok habis
    """

    return success_response(
        data=stok_habis()
    )


def get_dashboard_bi():
    """
    Endpoint lengkap BI
    Menggabungkan seluruh data dashboard
    agar frontend cukup memanggil 1 endpoint.
    """

    summary = summary_data()

    summary["omzet_hari_ini"] = omzet_hari_ini()
    summary["total_nasi_terjual"] = total_nasi_terjual()
    summary["total_item_terjual"] = total_item_terjual()

    return success_response(
        data={
            "summary": summary,
            "grafik_penjualan": chart_penjualan(),
            "lauk_terlaris": top_lauk(),
            "stok_habis": stok_habis()
        }
    )