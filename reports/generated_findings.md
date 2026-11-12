# Generated findings

Reproduce with `python src/analyze.py` from the repository root.

## Business insights

- **Scope:** 9,994 line items across 5,009 distinct orders,
  from 2014-01-03 to 2017-12-30.
- **Revenue:** $2,297,200.86; **profit:** $286,397.02;
  **profit margin:** 12.47% (total profit / total sales).
- **Lowest-profit subcategory:** Tables, with profit of
  $-17,725.48 on $206,965.53 revenue
  (-8.56% margin).
- **Lowest-margin region:** Central, with
  7.92% margin on $501,239.89 revenue.
- **Loss-making lines:** 1,871
  (18.72% of line items).

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
