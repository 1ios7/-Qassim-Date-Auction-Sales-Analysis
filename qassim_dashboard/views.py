import csv

from django.http import HttpResponse
from django.shortcuts import render


CITIES = ["بريدة", "عنيزة", "الرس", "المذنب", "البكيرية"]


BRANCH_DATA = {
    "بريدة": [
        {"deal_id": 1001, "product": "سكري فاخر", "category": "تمور", "price": 18500, "quantity": 42, "status": "تم البيع"},
        {"deal_id": 1002, "product": "خلاص القصيم", "category": "تمور", "price": 13200, "quantity": 35, "status": "تم البيع"},
        {"deal_id": 1003, "product": "صقعي ممتاز", "category": "تمور", "price": 9700, "quantity": 22, "status": "تم البيع"},
        {"deal_id": 1004, "product": "برحي طازج", "category": "تمور", "price": 7600, "quantity": 18, "status": "تم البيع"},
        {"deal_id": 1005, "product": "تمر مجدول", "category": "تمور", "price": 15400, "quantity": 26, "status": "تم البيع"},
    ],
    "عنيزة": [
        {"deal_id": 2001, "product": "سكري عضوي", "category": "تمور", "price": 22400, "quantity": 38, "status": "تم البيع"},
        {"deal_id": 2002, "product": "خلاص ممتاز", "category": "تمور", "price": 14100, "quantity": 31, "status": "تم البيع"},
        {"deal_id": 2003, "product": "عجوة فاخرة", "category": "تمور", "price": 17600, "quantity": 24, "status": "تم البيع"},
        {"deal_id": 2004, "product": "سكري مفتل", "category": "تمور", "price": 19800, "quantity": 29, "status": "تم البيع"},
        {"deal_id": 2005, "product": "رطب برحي", "category": "تمور", "price": 8300, "quantity": 19, "status": "تم البيع"},
    ],
    "الرس": [
        {"deal_id": 3001, "product": "سكري فاخر", "category": "تمور", "price": 12800, "quantity": 28, "status": "تم البيع"},
        {"deal_id": 3002, "product": "خلاص الرس", "category": "تمور", "price": 9400, "quantity": 24, "status": "تم البيع"},
        {"deal_id": 3003, "product": "صقعي", "category": "تمور", "price": 7200, "quantity": 17, "status": "تم البيع"},
        {"deal_id": 3004, "product": "تمر شعبي", "category": "تمور", "price": 5100, "quantity": 15, "status": "تم البيع"},
        {"deal_id": 3005, "product": "سكري مفتل", "category": "تمور", "price": 11600, "quantity": 21, "status": "تم البيع"},
    ],
    "المذنب": [
        {"deal_id": 4001, "product": "خلاص المذنب", "category": "تمور", "price": 8700, "quantity": 20, "status": "تم البيع"},
        {"deal_id": 4002, "product": "سكري متوسط", "category": "تمور", "price": 10300, "quantity": 23, "status": "تم البيع"},
        {"deal_id": 4003, "product": "برحي", "category": "تمور", "price": 6800, "quantity": 16, "status": "تم البيع"},
        {"deal_id": 4004, "product": "صقعي ممتاز", "category": "تمور", "price": 9100, "quantity": 19, "status": "تم البيع"},
        {"deal_id": 4005, "product": "تمر مجدول", "category": "تمور", "price": 12200, "quantity": 18, "status": "تم البيع"},
    ],
    "البكيرية": [
        {"deal_id": 5001, "product": "سكري فاخر", "category": "تمور", "price": 14900, "quantity": 30, "status": "تم البيع"},
        {"deal_id": 5002, "product": "خلاص ممتاز", "category": "تمور", "price": 11200, "quantity": 27, "status": "تم البيع"},
        {"deal_id": 5003, "product": "رطب برحي", "category": "تمور", "price": 7900, "quantity": 18, "status": "تم البيع"},
        {"deal_id": 5004, "product": "عجوة", "category": "تمور", "price": 13500, "quantity": 22, "status": "تم البيع"},
        {"deal_id": 5005, "product": "صقعي", "category": "تمور", "price": 8600, "quantity": 20, "status": "تم البيع"},
    ],
}


MONTHLY_BRANCH_PERFORMANCE = {
    "بريدة": [82000, 91000, 105000, 118000, 126000, 139000],
    "عنيزة": [76000, 88000, 97000, 112000, 124000, 148000],
    "الرس": [52000, 61000, 69000, 78000, 85000, 92000],
    "المذنب": [47000, 54000, 61000, 69000, 74000, 81000],
    "البكيرية": [59000, 67000, 72000, 84000, 93000, 103000],
}


def dashboard_home(request):
    selected_city = request.GET.get("city", "بريدة")

    if selected_city not in CITIES:
        selected_city = "بريدة"

    deals = BRANCH_DATA[selected_city]

    total_sales = sum(item["price"] for item in deals)
    total_quantity = sum(item["quantity"] for item in deals)
    deals_count = len(deals)
    average_deal = round(total_sales / deals_count, 2) if deals_count else 0
    top_deal = max(deals, key=lambda x: x["price"]) if deals else None

    product_labels = [item["product"] for item in deals]
    product_values = [item["price"] for item in deals]
    quantity_values = [item["quantity"] for item in deals]

    all_branch_totals = []
    for city in CITIES:
        city_total = sum(item["price"] for item in BRANCH_DATA[city])
        all_branch_totals.append(city_total)

    monthly_labels = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو"]
    monthly_values = MONTHLY_BRANCH_PERFORMANCE[selected_city]

    market_share_total = sum(all_branch_totals)
    selected_total = total_sales
    market_share = round((selected_total / market_share_total) * 100, 1) if market_share_total else 0

    context = {
        "cities": CITIES,
        "selected_city": selected_city,
        "deals": deals,
        "total_sales": total_sales,
        "total_quantity": total_quantity,
        "deals_count": deals_count,
        "average_deal": average_deal,
        "top_deal": top_deal,
        "product_labels": product_labels,
        "product_values": product_values,
        "quantity_values": quantity_values,
        "branch_labels": CITIES,
        "branch_values": all_branch_totals,
        "monthly_labels": monthly_labels,
        "monthly_values": monthly_values,
        "market_share": market_share,
    }

    return render(request, "qassim_dashboard/dashboard.html", context)


def download_report(request):
    selected_city = request.GET.get("city", "بريدة")

    if selected_city not in CITIES:
        selected_city = "بريدة"

    deals = BRANCH_DATA[selected_city]

    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = f'attachment; filename="qassim_dashboard_{selected_city}.csv"'

    response.write("\ufeff")
    writer = csv.writer(response)

    writer.writerow(["رقم الصفقة", "المنتج", "التصنيف", "السعر", "الكمية", "الحالة", "الفرع"])

    for item in deals:
        writer.writerow([
            item["deal_id"],
            item["product"],
            item["category"],
            item["price"],
            item["quantity"],
            item["status"],
            selected_city,
        ])

    return response