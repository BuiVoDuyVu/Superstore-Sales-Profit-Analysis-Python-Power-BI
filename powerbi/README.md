# Power BI Dashboard

Open [Superstore_Dashboard.pbix](Superstore_Dashboard.pbix) in Microsoft Power BI Desktop to inspect the supplied report. Python prepares the transaction table; Power BI provides a place to explore the results by time, region, category, and discount band.

The PBIX is a desktop deliverable. Refresh success, filter interactions, and reconciliation should be checked in Power BI Desktop using the steps below. No Power BI Service deployment or public interactive report is claimed.

## Refresh after cloning

Power BI may retain an absolute path from the original author's computer. Repoint that connection before refreshing:

1. From the repository root, generate [data/processed/superstore_clean.csv](../data/processed/superstore_clean.csv) with the [Python analysis](../src/analyze.py) using the setup commands in the [main README](../README.md).
2. Open the PBIX in Power BI Desktop.
3. Select **File → Options and settings → Data source settings**. Choose the CSV connection and select **Change Source**; browse to the prepared CSV in your local clone.
4. If **Change Source** is unavailable, open **Transform data** and inspect the affected query's **Source** step. Update the path there, or edit the `File.Contents(...)` path in **Advanced Editor**.
5. Review the query steps and column types, then select **Close & Apply → Refresh**. Resolve any missing-column or path errors before interpreting the visuals.

Use the cleaned transaction table as the analytical source. Aggregated summary CSVs are useful for reconciliation, but importing them into the same table would change its grain.

## Table and field configuration

The formulas in [measures.dax](measures.dax) assume the transaction table is named **Superstore**. Rename the imported table or adjust the formulas to your actual table name.

| Fields | Power BI type or format |
|---|---|
| `Order Date`, `Ship Date` | Date; the prepared CSV uses ISO `YYYY-MM-DD` |
| `Sales`, `Profit` | Decimal number; currency display in USD |
| `Discount` | Decimal number; format as Percentage for display |
| `Quantity`, `Year`, `Loss Line` | Whole number |
| `Postal Code`, order/customer/product identifiers | Text |
| `YearMonth`, `Region`, `Category`, `Sub-Category`, `Discount Group` | Text |

The prepared table is sufficient for the documented analysis. Do not create a relationship between `Order ID` and `Row ID` inside the same table. For additional time-intelligence measures, a dedicated date table can be added later.

## Measures

Create each expression separately with **Modeling → New measure**, using [measures.dax](measures.dax) as the reference:

- **Total Sales**, **Total Profit**, and **Average Order Value**: format as USD currency.
- **Profit Margin**: format as Percentage with two decimal places. The formula returns a ratio; do not multiply it by 100 in DAX when applying percentage formatting.
- **Total Orders**, **Total Quantity**, and **Loss-Making Lines**: format as whole numbers.

`Total Orders` uses a distinct count. `Profit Margin` divides aggregate profit by aggregate sales within the current filter context. Its zero-revenue fallback is 0; the Python summary tables instead leave that case missing.

## Suggested analytical navigation

Use the supplied report as the starting point and inspect its actual pages in Desktop. The following views organize the business questions; they are also a checklist for extending the report.

| View | Useful visuals | Question answered |
|---|---|---|
| Executive overview | Sales, profit, margin, and order cards; monthly revenue trend; revenue and profit by region; profit by category | How large is the business, and where is profitability strongest or weakest? |
| Profitability detail | Profit by subcategory; weighted margin by discount band; region × category matrix; loss-making-line card | Which combinations deserve investigation and a controlled business test? |

Useful slicers include `Year`, `Region`, `Category`, and `Segment`. Preserve chronological ordering for monthly charts. For discount charts, use **0% → (0%, 20%] → (20%, 40%] → >40%** instead of alphabetical order. If needed, create a calculated sort column and apply **Sort by column**:

```DAX
Discount Band Sort =
SWITCH(
    Superstore[Discount Group],
    "0%", 1,
    "(0%, 20%]", 2,
    "(20%, 40%]", 3,
    ">40%", 4,
    5
)
```

Use a consistent currency unit, readable labels, and a clear negative-value color. Discount comparisons describe an observed association, not proof that changing a discount would cause the observed profit difference.

## Manual reconciliation checklist

These are checks for the reviewer to perform in Power BI Desktop; unchecked items are not a claim of completed validation.

- [ ] All sources point to the local clone and refresh without errors.
- [ ] With all slicers and report/page/visual filters cleared, cards match the [KPI export](../reports/tables/kpi.json): **$2,297,200.86 sales**, **$286,397.02 profit**, **12.47% margin**, **5,009 orders**, **37,873 units**, and **1,871 loss-making lines**.
- [ ] Filtering to Central matches **$501,239.89 sales**, **$39,706.36 profit**, and **7.92% margin** in the [regional summary](../reports/tables/summary_region.csv).
- [ ] Subcategory totals reconcile to the [subcategory summary](../reports/tables/summary_subcategory.csv), including Tables at **−$17,725.48** profit.
- [ ] Discount bands follow the intended order and reconcile to the [discount summary](../reports/tables/summary_discount_group.csv).
- [ ] Slicers affect the intended cards, charts, and matrix; clear each slicer and confirm the totals return to the baseline.
- [ ] Monthly values reconcile to the [monthly summary](../reports/tables/summary_monthly.csv); dates are parsed and sorted correctly.
- [ ] Saved screenshots or PDF exports state their filter context and match the refreshed report.

For interpretation and proposed actions, see [Business Insights & Recommendations](../docs/business_insights.md). The existing [project report](../reports/Superstore_Project_Report.pdf) is provided as a separate deliverable.
