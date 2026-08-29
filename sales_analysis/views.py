import csv
import json
import os

import pandas as pd
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def _data_file_path():
    return os.path.join(settings.BASE_DIR, "sales_analysis", "data", "sales_data_sample.csv")


def _load_sales_data():
    file_path = _data_file_path()

    try:
        df = pd.read_csv(file_path, encoding="latin1")
    except Exception:
        return None

    df = df.fillna("")
    return df


def _safe_number(value):
    try:
        return round(float(value), 2)
    except Exception:
        return 0


def dashboard_home(request):
    df = _load_sales_data()

    if df is None or df.empty:
        return render(request, "sales_analysis/dashboard.html", {
            "status": "error",
        })

    total_rows = len(df)
    total_columns = len(df.columns)

    sales_col = "SALES" if "SALES" in df.columns else None
    quantity_col = "QUANTITYORDERED" if "QUANTITYORDERED" in df.columns else None
    price_col = "PRICEEACH" if "PRICEEACH" in df.columns else None
    product_col = "PRODUCTLINE" if "PRODUCTLINE" in df.columns else None
    country_col = "COUNTRY" if "COUNTRY" in df.columns else None
    status_col = "STATUS" if "STATUS" in df.columns else None
    year_col = "YEAR_ID" if "YEAR_ID" in df.columns else None
    month_col = "MONTH_ID" if "MONTH_ID" in df.columns else None
    deal_size_col = "DEALSIZE" if "DEALSIZE" in df.columns else None
    customer_col = "CUSTOMERNAME" if "CUSTOMERNAME" in df.columns else None

    total_sales = _safe_number(df[sales_col].sum()) if sales_col else 0
    total_quantity = int(df[quantity_col].sum()) if quantity_col else 0
    average_order_value = _safe_number(df[sales_col].mean()) if sales_col else 0
    max_order_value = _safe_number(df[sales_col].max()) if sales_col else 0

    unique_customers = df[customer_col].nunique() if customer_col else 0
    unique_countries = df[country_col].nunique() if country_col else 0
    unique_products = df[product_col].nunique() if product_col else 0

    top_products = []
    if sales_col and product_col:
        grouped = (
            df.groupby(product_col)[sales_col]
            .sum()
            .sort_values(ascending=False)
            .head(7)
        )
        top_products = [{"label": str(k), "value": _safe_number(v)} for k, v in grouped.items()]

    country_sales = []
    if sales_col and country_col:
        grouped = (
            df.groupby(country_col)[sales_col]
            .sum()
            .sort_values(ascending=False)
            .head(7)
        )
        country_sales = [{"label": str(k), "value": _safe_number(v)} for k, v in grouped.items()]

    status_distribution = []
    if status_col:
        grouped = df[status_col].value_counts().head(6)
        status_distribution = [{"label": str(k), "value": int(v)} for k, v in grouped.items()]

    deal_size_sales = []
    if sales_col and deal_size_col:
        grouped = (
            df.groupby(deal_size_col)[sales_col]
            .sum()
            .sort_values(ascending=False)
        )
        deal_size_sales = [{"label": str(k), "value": _safe_number(v)} for k, v in grouped.items()]

    monthly_sales = []
    if sales_col and year_col and month_col:
        monthly_df = (
            df.groupby([year_col, month_col])[sales_col]
            .sum()
            .reset_index()
            .sort_values([year_col, month_col])
        )
        monthly_sales = [
            {
                "label": f"{int(row[month_col])}/{int(row[year_col])}",
                "value": _safe_number(row[sales_col]),
            }
            for _, row in monthly_df.iterrows()
        ]

    preview_columns = list(df.columns[:8])
    preview_rows = []
    for _, row in df.head(10).iterrows():
        preview_rows.append([row[col] for col in preview_columns])

    top_product_name = top_products[0]["label"] if top_products else "غير متاح"
    top_country_name = country_sales[0]["label"] if country_sales else "غير متاح"

    context = {
        "status": "success",

        "total_rows": total_rows,
        "total_columns": total_columns,
        "total_sales": total_sales,
        "total_quantity": total_quantity,
        "average_order_value": average_order_value,
        "max_order_value": max_order_value,
        "unique_customers": unique_customers,
        "unique_countries": unique_countries,
        "unique_products": unique_products,
        "top_product_name": top_product_name,
        "top_country_name": top_country_name,

        "preview_columns": preview_columns,
        "preview_rows": preview_rows,

        "top_products_labels": json.dumps([x["label"] for x in top_products], ensure_ascii=False),
        "top_products_values": json.dumps([x["value"] for x in top_products], ensure_ascii=False),

        "country_sales_labels": json.dumps([x["label"] for x in country_sales], ensure_ascii=False),
        "country_sales_values": json.dumps([x["value"] for x in country_sales], ensure_ascii=False),

        "status_labels": json.dumps([x["label"] for x in status_distribution], ensure_ascii=False),
        "status_values": json.dumps([x["value"] for x in status_distribution], ensure_ascii=False),

        "deal_size_labels": json.dumps([x["label"] for x in deal_size_sales], ensure_ascii=False),
        "deal_size_values": json.dumps([x["value"] for x in deal_size_sales], ensure_ascii=False),

        "monthly_labels": json.dumps([x["label"] for x in monthly_sales], ensure_ascii=False),
        "monthly_values": json.dumps([x["value"] for x in monthly_sales], ensure_ascii=False),
    }

    return render(request, "sales_analysis/dashboard.html", context)


def download_sales_csv(request):
    df = _load_sales_data()

    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = 'attachment; filename="sales_analysis_report.csv"'
    response.write("\ufeff")

    writer = csv.writer(response)

    if df is None or df.empty:
        writer.writerow(["No data available"])
        return response

    writer.writerow(list(df.columns))

    for _, row in df.iterrows():
        writer.writerow([row[col] for col in df.columns])

    return response