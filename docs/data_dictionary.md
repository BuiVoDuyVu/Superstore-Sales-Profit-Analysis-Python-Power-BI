# Data Dictionary

## Source, scope, and grain

- **Dataset:** Tableau Sample – Superstore, an educational retail dataset.
- **Official sample-data reference:** [Tableau Public sample data](https://public.tableau.com/app/learn/sample-data).
- **CSV used:** [SharmaAshwini's Superstore Gist](https://gist.github.com/SharmaAshwini/8bd642f6c46792a9c40c8ccad60391e9), pinned to revision `4fd45d58a0a81c69814d270d7658f5e2a2d81154` by the [download script](../src/download_data.py).
- **Raw file:** [Sample_Superstore.csv](../data/raw/Sample_Superstore.csv).
- **Prepared file:** [superstore_clean.csv](../data/processed/superstore_clean.csv).
- **Observed scope:** 9,994 line items, 21 raw fields, 2014-01-03–2017-12-30; see the [quality report](../reports/data_quality/data_quality.json).

**One row represents one product line within an order.** `Order ID` and `Customer ID` can repeat. Use distinct `Order ID` values to count orders. `Row ID` identifies the line item and has no duplicates in this snapshot. Do not use `Product ID` as a row identifier.

The source remains attributed to Tableau and the CSV mirror. No independent dataset license is asserted here; consult the source's terms when redistributing or reusing it.

## Original fields

Types describe the intended analytical interpretation after preparation. The original CSV stores dates as text and contains no explicit schema.

| Field | Analytical type | Description and treatment |
|---|---|---|
| `Row ID` | Integer identifier | Source line-item identifier. Duplicate identifiers are reported by the quality checks. |
| `Order ID` | Text identifier | Order reference; repeated values are expected for orders with multiple product lines. |
| `Order Date` | Date | Order placement date. The selected mirror uses `DD/MM/YY`; prepared CSV dates use `YYYY-MM-DD`. Drives time grouping. |
| `Ship Date` | Date | Shipment date. Parsed using the selected date convention when present; invalid shipping dates are not a separate rejection criterion in the current pipeline. |
| `Ship Mode` | Categorical text | Shipping service class, such as Standard Class or Second Class. |
| `Customer ID` | Text identifier | Customer reference. Use distinct values to count customers. |
| `Customer Name` | Text | Customer display name supplied by the educational dataset. |
| `Segment` | Categorical text | Customer segment, such as Consumer, Corporate, or Home Office. |
| `Country` | Categorical text | Country recorded for the transaction. |
| `City` | Categorical text | City recorded for the transaction. |
| `State` | Categorical text | State recorded for the transaction. |
| `Postal Code` | Text identifier | Postal code. Read as a string to preserve identifier formatting and any leading zeros. Do not sum or average it. |
| `Region` | Categorical text | Sales region: Central, East, South, or West in this snapshot. |
| `Product ID` | Text identifier | Product reference; products can appear in multiple orders and rows. |
| `Category` | Categorical text | Main product category: Furniture, Office Supplies, or Technology. |
| `Sub-Category` | Categorical text | More detailed product grouping, such as Tables or Copiers. |
| `Product Name` | Text | Product description supplied by the source. |
| `Sales` | Decimal, USD | Revenue value recorded for the line item. Used as supplied; the pipeline does not apply the discount again. Values below zero are rejected from analysis. |
| `Quantity` | Numeric count | Number of units on the line item; non-positive values are rejected. The current checks do not separately enforce integer-valued counts. |
| `Discount` | Decimal proportion | Recorded discount from 0 to 1; `0.20` means 20%. Values outside this range are rejected. |
| `Profit` | Decimal, USD | Profit value supplied for the line item. Negative values are valid and retained. Detailed cost components cannot be reconstructed from this field alone. |

## Engineered fields

The [analysis script](../src/analyze.py) appends these four columns to the prepared dataset.

| Field | Type | Definition |
|---|---|---|
| `Year` | Integer | Calendar year of `Order Date`. |
| `YearMonth` | Text, `YYYY-MM` | Calendar month of `Order Date`; sortable in chronological order as formatted. |
| `Discount Group` | Categorical text | `0%` when discount equals 0; `(0%, 20%]` when 0 < discount ≤ 0.20; `(20%, 40%]` when 0.20 < discount ≤ 0.40; `>40%` when discount > 0.40. |
| `Loss Line` | Integer flag | 1 when `Profit < 0`; otherwise 0. Summing this flag counts loss-making line items. |

## Cleaning and quality rules

1. Read the CSV with UTF-8 BOM handling; trim column-name whitespace and remove a column-name BOM if present.
2. Require `Order ID`, `Order Date`, `Region`, `Category`, `Sub-Category`, `Sales`, `Profit`, `Discount`, and `Quantity`.
3. Record source missing-cell counts, exact duplicate rows, and duplicate `Row ID` values when available. Duplicate checks are diagnostic; they do not automatically delete rows.
4. Select the date format from the order-date sample: the selected two-digit-year source uses `%d/%m/%y`; the supported four-digit-year alternative uses `%m/%d/%Y`. This is not a parser for arbitrary date formats.
5. Convert dates and numerical analysis fields; unparseable values become missing.
6. Exclude records missing any required field, or with `Sales < 0`, `Quantity <= 0`, or `Discount` outside [0, 1]. Retain valid negative profits and repeated order references.
7. Export excluded rows to the [quality-issues CSV](../reports/data_quality/data_quality_issues.csv), and record the audit summary in the [quality JSON](../reports/data_quality/data_quality.json).

The current snapshot has **zero excluded rows**. These checks do not establish that every business value is accurate; they document the implemented validation scope.

## KPI and aggregate definitions

| Output measure | Formula | Interpretation |
|---|---|---|
| Revenue / `Revenue` | `SUM(Sales)` | Total recorded line revenue. |
| Profit / `Profit` | `SUM(Profit)` | Total supplied line profit. |
| Profit margin / `Profit_Margin_Pct` | `SUM(Profit) / SUM(Sales) × 100` | Weighted aggregate margin. The analytical summaries use a missing value if revenue is zero. |
| Orders / `distinct_orders` | `COUNT DISTINCT(Order ID)` | Unique orders, not transaction rows. |
| Customers / `distinct_customers` | `COUNT DISTINCT(Customer ID)` | Unique customer identifiers when the column exists. |
| Line items / `Line_Items` | Number of rows | Transaction-line count. |
| Quantity / `Quantity` | `SUM(Quantity)` | Units sold. |
| Loss-making lines / `Loss_Lines` | `SUM(Loss Line)` | Number of rows with negative profit. |
| Average order value | `SUM(Sales) / COUNT DISTINCT(Order ID)` | Revenue per distinct order; provided as a Power BI measure. |

The [KPI JSON](../reports/tables/kpi.json) reports the whole dataset. The [summary tables](../reports/tables/) apply the same aggregation logic within each grouping. Monetary values are USD; percentages in analytical tables are on a 0–100 scale, while the Power BI `Profit Margin` measure is a decimal ratio formatted as Percentage.
