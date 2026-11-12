"""End-to-end exploratory analysis of Sample Superstore (educational demo).

Run from the repository root: python src/analyze.py
Requires data/raw/Sample_Superstore.csv (from src/download_data.py or manual download).
This code intentionally flags suspected issues instead of silently dropping data.
"""
from pathlib import Path
import json
import matplotlib
if __name__ == "__main__":
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
INPUT = BASE / "data" / "raw" / "Sample_Superstore.csv"
PROCESSED = BASE / "data" / "processed"
REPORTS = BASE / "reports"
QUALITY = REPORTS / "data_quality"
TABLES = REPORTS / "tables"
FIGURES = REPORTS / "figures"
REQUIRED = [
    "Order ID", "Order Date", "Region", "Category", "Sub-Category",
    "Sales", "Profit", "Discount", "Quantity"
]


def read_and_clean(path):
    if not path.exists():
        raise FileNotFoundError(
            f"Chưa có {path.name}. Chạy: python src/download_data.py "
            "hoặc tải CSV thủ công vào thư mục data/raw/."
        )
    raw = pd.read_csv(path, encoding="utf-8-sig", low_memory=False,
                      dtype={"Postal Code": "string"})
    raw.columns = raw.columns.str.replace("\ufeff", "", regex=False).str.strip()
    missing = [c for c in REQUIRED if c not in raw.columns]
    if missing:
        raise ValueError(f"Thiếu các cột bắt buộc: {missing}")

    df = raw.copy()
    checks = {
        "raw_rows": len(df),
        "raw_columns": len(df.columns),
        "null_cells_by_column": {str(k): int(v) for k, v in df.isna().sum().items()},
        "exact_duplicate_rows": int(df.duplicated().sum()),
        "duplicate_row_ids": (int(df["Row ID"].duplicated().sum())
                              if "Row ID" in df.columns else None)
    }
    # Date convention: selected Gist CSV uses DD/MM/YY (e.g., 15/04/17).
    # A 4-digit-year CSV mirror often uses MM/DD/YYYY. Detect carefully.
    date_sample = df["Order Date"].dropna().astype(str)
    if date_sample.empty:
        raise ValueError("Không có ngày đặt hàng để phân tích.")
    date_format = "%d/%m/%y" if date_sample.str.contains(r"/\d{2}$").mean() > 0.8 else "%m/%d/%Y"
    for col in ["Order Date", "Ship Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format=date_format, errors="coerce")
    for col in ["Sales", "Profit", "Discount", "Quantity"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    invalid_mask = (
        df[REQUIRED].isna().any(axis=1)
        | (df["Sales"] < 0)
        | (df["Quantity"] <= 0)
        | (df["Discount"] < 0)
        | (df["Discount"] > 1)
    )
    invalid = df.loc[invalid_mask].copy()
    checks.update({
        "date_format_used": date_format,
        "invalid_rows_removed_from_analysis": len(invalid),
        "invalid_date_values": int(df["Order Date"].isna().sum()),
    })
    df = df.loc[~invalid_mask].copy()
    if df.empty:
        raise ValueError("Không còn dòng dữ liệu hợp lệ. Kiểm tra định dạng ngày.")

    df["Year"] = df["Order Date"].dt.year
    df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Discount Group"] = np.select(
        [df["Discount"] == 0, df["Discount"].between(0, .2, inclusive="right"),
         df["Discount"].between(.2, .4, inclusive="right"), df["Discount"] > .4],
        ["0%", "(0%, 20%]", "(20%, 40%]", ">40%"],
        default="Other"
    )
    df["Loss Line"] = (df["Profit"] < 0).astype(int)
    checks["clean_rows"] = len(df)
    checks["min_order_date"] = str(df["Order Date"].min().date())
    checks["max_order_date"] = str(df["Order Date"].max().date())
    return df, invalid, checks


def summarize(df, keys):
    summary = df.groupby(keys, dropna=False).agg(
        Line_Items=("Order ID", "size"),
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Loss_Lines=("Loss Line", "sum"),
    ).reset_index()
    summary["Profit_Margin_Pct"] = np.where(
        summary["Revenue"] != 0, summary["Profit"] / summary["Revenue"] * 100, np.nan
    )
    return summary


def make_bar(data, label, value, title, outpath, sort=True, horizontal=True):
    temp = data.sort_values(value, ascending=True if horizontal else False) if sort else data
    fig, ax = plt.subplots(figsize=(10, 5.5))
    if horizontal:
        ax.barh(temp[label].astype(str), temp[value])
        ax.axvline(0, color="black", linewidth=0.8)
    else:
        ax.bar(temp[label].astype(str), temp[value])
        ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title(title)
    ax.set_xlabel(value.replace("_", " "))
    fig.tight_layout()
    fig.savefig(outpath, dpi=160)
    plt.close(fig)


def main():
    for directory in [PROCESSED, QUALITY, TABLES, FIGURES]:
        directory.mkdir(parents=True, exist_ok=True)
    df, invalid, checks = read_and_clean(INPUT)
    df.to_csv(PROCESSED / "superstore_clean.csv", index=False, encoding="utf-8-sig",
              date_format="%Y-%m-%d")
    invalid.to_csv(QUALITY / "data_quality_issues.csv", index=False, encoding="utf-8-sig")
    (QUALITY / "data_quality.json").write_text(
        json.dumps(checks, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    total_sales, total_profit = float(df["Sales"].sum()), float(df["Profit"].sum())
    metrics = {
        "line_items": int(len(df)),
        "distinct_orders": int(df["Order ID"].nunique()),
        "distinct_customers": (int(df["Customer ID"].nunique())
                               if "Customer ID" in df else None),
        "revenue": total_sales,
        "profit": total_profit,
        "profit_margin_pct": total_profit / total_sales * 100 if total_sales else None,
        "quantity": int(df["Quantity"].sum()),
        "loss_making_lines": int((df["Profit"] < 0).sum()),
    }
    (TABLES / "kpi.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    outputs = {
        "region": summarize(df, ["Region"]),
        "category": summarize(df, ["Category"]),
        "subcategory": summarize(df, ["Category", "Sub-Category"]),
        "discount_group": summarize(df, ["Discount Group"]),
        "monthly": summarize(df, ["YearMonth"]),
        "region_category": summarize(df, ["Region", "Category"]),
        "yearly": summarize(df, ["Year"]),
    }
    for k, tbl in outputs.items():
        tbl.to_csv(TABLES / f"summary_{k}.csv", index=False, encoding="utf-8-sig")

    make_bar(outputs["region"], "Region", "Profit", "Profit by Region", FIGURES / "01_profit_by_region.png")
    sub = outputs["subcategory"].copy()
    make_bar(sub, "Sub-Category", "Profit", "Profit by Sub-Category", FIGURES / "02_profit_by_subcategory.png")
    discount = outputs["discount_group"].set_index("Discount Group").reindex(
        ["0%", "(0%, 20%]", "(20%, 40%]", ">40%"]
    ).reset_index()
    make_bar(discount, "Discount Group", "Profit_Margin_Pct", "Profit Margin by Discount Band (%)",
             FIGURES / "03_margin_by_discount.png", sort=False, horizontal=False)
    fig, ax = plt.subplots(figsize=(11, 5))
    monthly = outputs["monthly"].sort_values("YearMonth")
    ax.plot(monthly["YearMonth"], monthly["Revenue"], marker=".")
    ax.set_title("Monthly Revenue")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x", rotation=75)
    ax.set_xticks(monthly["YearMonth"].iloc[::max(1, len(monthly) // 12)])
    fig.tight_layout()
    fig.savefig(FIGURES / "04_monthly_revenue.png", dpi=160)
    plt.close(fig)

    worst_sub = sub.loc[sub["Profit"].idxmin()]
    region_low = outputs["region"].loc[outputs["region"]["Profit_Margin_Pct"].idxmin()]
    notes = f"""# Generated findings

Reproduce with `python src/analyze.py` from the repository root.

## Business insights

- **Scope:** {metrics['line_items']:,} line items across {metrics['distinct_orders']:,} distinct orders,
  from {checks['min_order_date']} to {checks['max_order_date']}.
- **Revenue:** ${total_sales:,.2f}; **profit:** ${total_profit:,.2f};
  **profit margin:** {metrics['profit_margin_pct']:.2f}% (total profit / total sales).
- **Lowest-profit subcategory:** {worst_sub['Sub-Category']}, with profit of
  ${worst_sub['Profit']:,.2f} on ${worst_sub['Revenue']:,.2f} revenue
  ({worst_sub['Profit_Margin_Pct']:.2f}% margin).
- **Lowest-margin region:** {region_low['Region']}, with
  {region_low['Profit_Margin_Pct']:.2f}% margin on ${region_low['Revenue']:,.2f} revenue.
- **Loss-making lines:** {metrics['loss_making_lines']:,}
  ({metrics['loss_making_lines'] / metrics['line_items'] * 100:.2f}% of line items).

Evidence: [KPI totals](tables/kpi.json), [regional summary](tables/summary_region.csv),
[subcategory summary](tables/summary_subcategory.csv),
[discount bands](tables/summary_discount_group.csv).

## Business recommendations

1. Prioritize a review of prices, discounts, and product mix in the lowest-profit
   subcategory and the lowest-margin region. Use the
   [region/category breakdown](tables/summary_region_category.csv) and detailed rows
   in Power BI to distinguish product-mix effects from regional performance.
2. Pilot discount guardrails within comparable products and regions. Track profit,
   revenue, quantity, and loss-making line share against a comparison group before
   extending any policy. Observed discount/margin associations do not establish causality.
3. Monitor aggregate margin and loss-making line share alongside revenue in a monthly
   business review. These are proposed actions; no intervention or measured uplift is claimed.

Sample Superstore is an educational sample, not evidence about a real business.
The Profit field does not provide a detailed cost breakdown.
"""
    (REPORTS / "generated_findings.md").write_text(notes, encoding="utf-8")

    print("===== KET QUA TONG QUAN =====")
    for k,v in metrics.items():
        print(f"{k}: {v}")
    print("\nCleaned data:", PROCESSED)
    print("Reports, tables, and figures:", REPORTS)


if __name__ == "__main__":
    main()
