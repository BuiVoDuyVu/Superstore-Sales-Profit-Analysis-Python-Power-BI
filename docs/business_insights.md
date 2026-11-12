# Business Insights & Recommendations

This analysis examines where sales translate into profit, where losses concentrate, and which decisions deserve further testing. The scope is Tableau's historical Sample Superstore dataset, covering **3 January 2014–30 December 2017**. It is an educational retail sample, not a current operating company report.

The workflow is **Data Cleaning → EDA → Data Visualization → Business Insights → Business Recommendations**. Findings below are tied to exported analytical tables; recommendations are proposed actions, not measured business outcomes.

## Measurement basis

| Metric | Result | Definition |
|---|---:|---|
| Revenue | $2,297,200.86 | Sum of `Sales` |
| Profit | $286,397.02 | Sum of `Profit` |
| Profit margin | 12.47% | Total profit / total revenue × 100 |
| Orders | 5,009 | Distinct `Order ID` values |
| Customers | 793 | Distinct `Customer ID` values |
| Line items | 9,994 | Number of transaction lines |
| Units sold | 37,873 | Sum of `Quantity` |
| Loss-making line items | 1,871 | Lines where `Profit < 0` |

Source: [KPI export](../reports/tables/kpi.json). Monetary results are in USD and rounded for display; the exports retain analytical precision. A line item is not an order. Profit margin is calculated from aggregate totals, never by averaging individual line margins.

The [quality report](../reports/data_quality/data_quality.json) records 9,994 source rows and 21 source columns, with no missing cells, exact duplicate rows, duplicate row identifiers, or rejected records in this snapshot. Cleaning standardizes types and adds analytical fields; negative profits are retained as valid observations.

## 1. Furniture has substantial sales but weak profitability

| Category | Revenue | Profit | Profit margin |
|---|---:|---:|---:|
| Furniture | $741,999.80 | $18,451.27 | 2.49% |
| Office Supplies | $719,047.03 | $122,490.80 | 17.04% |
| Technology | $836,154.03 | $145,454.95 | 17.40% |

Source: [category summary](../reports/tables/summary_category.csv).

Furniture's sales volume does not translate into comparable profit. Within Furniture, **Tables** produces $206,965.53 in revenue but **−$17,725.48** in profit, a **−8.56%** margin. **Bookcases** also records an aggregate loss of **−$3,472.56**. Outside Furniture, **Supplies** loses **−$1,189.10**. These are specific areas for review rather than reasons to discontinue an entire category.

Evidence: [subcategory summary](../reports/tables/summary_subcategory.csv) and [profit by subcategory](../reports/figures/02_profit_by_subcategory.png).

**Business implication:** Review product mix, pricing, and promotion patterns within the loss-making subcategories before pursuing additional revenue there. The dataset does not separate procurement, fulfillment, and operating costs, so the cause of each loss requires additional evidence.

## 2. Central needs a targeted category review

**Central** has the lowest regional profit margin at **7.92%**, compared with **14.94%** in **West**. Central's total profit remains positive at **$39,706.36**; its weakness is not uniform across its categories.

Within Central, **Furniture loses $2,871.05**, with a **−1.75%** margin, while Technology produces **$33,697.43** profit at a **19.77%** margin. This supports investigating the region/category combination instead of applying a blanket regional policy.

Evidence: [regional summary](../reports/tables/summary_region.csv), [region × category summary](../reports/tables/summary_region_category.csv), and [profit by region](../reports/figures/01_profit_by_region.png).

**Business implication:** Start the regional profitability review with Central Furniture and compare its products, discount bands, and dates with the other regions. Differences in customer and product mix may explain part of the regional gap.

## 3. Higher discount bands are associated with lower margins

| Discount band | Line items | Profit | Profit margin |
|---|---:|---:|---:|
| 0% | 4,798 | $320,987.60 | 29.51% |
| (0%, 20%] | 3,803 | $100,785.47 | 11.91% |
| (20%, 40%] | 460 | −$35,817.47 | −15.30% |
| >40% | 933 | −$99,558.59 | −77.40% |

Source: [discount-band summary](../reports/tables/summary_discount_group.csv) and [margin by discount](../reports/figures/03_margin_by_discount.png).

All **933** line items discounted above 40% have negative profit in this dataset. This makes deeply discounted transactions a priority for review.

**Business implication:** Introduce a candidate review rule for deep discounts, then assess it within product, region, and time segments. This is an **observed association, not a causal estimate**: the data does not show how the same product would have sold at a different discount. Product mix, geography, and timing can confound the relationship. The results do not establish 20% or 40% as an optimal discount threshold.

## 4. Revenue growth should be assessed alongside margin

Revenue increases from **$609,205.60 in 2016** to **$733,215.26 in 2017**, and profit increases from **$81,795.17** to **$93,439.27**. However, margin declines from **13.43%** to **12.74%**.

Evidence: [yearly summary](../reports/tables/summary_yearly.csv) and [monthly revenue chart](../reports/figures/04_monthly_revenue.png).

**Business implication:** Track profitable growth using revenue, profit, and weighted margin together. The historical trend alone cannot establish seasonality, marketing effectiveness, or a forecast.

## Prioritized recommendations

The owners below are suggested business roles. No pricing change, commercial experiment, or financial uplift has been implemented or measured in this project.

| Priority | Proposed action | Suggested owner | Metrics and validation plan |
|---|---|---|---|
| P1 | Review Tables and Bookcases, beginning with Central Furniture. Break losses down by product, region, discount band, and month; obtain actual cost and promotion context before changing the assortment. | Category manager with a finance analyst | Monitor profit, weighted margin, revenue, units, and distinct orders for the reviewed scope. Reconcile cost definitions and compare comparable periods and products before a decision. |
| P1 | Pilot an approval rule or revised promotion policy for selected deep-discount transactions. Choose the rule after examining category and regional differences. | Pricing or commercial manager | Compare a pilot with a suitable control or randomized allocation where feasible. Use profit as the primary outcome; monitor revenue, orders, and units as guardrails. Define the test duration, acceptable trade-offs, and decision rule before launch. |
| P2 | Add a regular profitability review in Power BI with filters for time, region, category, and discount band. Prioritize negative-profit segments for investigation. | BI analyst with a sales operations owner | Reconcile totals to the Python exports after each refresh. Monitor weighted margin and loss-making lines, then validate any alert against the underlying transactions before escalation. |
| P2 | Investigate the 2017 margin decline before setting growth targets. Separate changes in product mix, region mix, and discounts from changes within comparable segments. | Finance or business planning analyst | Review monthly revenue and profit together. Compare weighted margins within the same segments; obtain promotion and cost data to test possible explanations. |

## Limits and next steps

- The dataset is a historical educational sample. Findings describe this snapshot and do not establish current retail market conditions.
- Profit is supplied by the source. Detailed cost components, campaign exposure, conversion, inventory availability, and alternative prices are unavailable.
- Aggregated margins can reflect product or regional mix. Check within-category and within-region results before recommending a broad policy.
- Any estimate of future savings or profit improvement requires explicit assumptions and additional evidence. No uplift is claimed here.

For the field definitions, see the [data dictionary](data_dictionary.md). For report setup and manual reconciliation, see the [Power BI guide](../powerbi/README.md).
