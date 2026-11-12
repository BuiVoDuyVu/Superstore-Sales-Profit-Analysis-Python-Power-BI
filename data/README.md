# Data provenance and usage

## Source

- Dataset: **Tableau Sample – Superstore**, a historical educational retail sample.
- CSV mirror: [SharmaAshwini / Sample_Superstore.csv](https://gist.github.com/SharmaAshwini/8bd642f6c46792a9c40c8ccad60391e9).
- Pinned mirror revision: `4fd45d58a0a81c69814d270d7658f5e2a2d81154`.
- [Pinned raw download](https://gist.githubusercontent.com/SharmaAshwini/8bd642f6c46792a9c40c8ccad60391e9/raw/4fd45d58a0a81c69814d270d7658f5e2a2d81154/Sample_Superstore.csv).
- Canonical file: [raw/Sample_Superstore.csv](raw/Sample_Superstore.csv).
- Original local source file SHA-256: `a798cff935a7ffa8032b793d6116eb87f6cb9e371b0f286267d9f10abb0ba00a` (original bytes, before any Git line-ending normalization).

The analysis uses 9,994 order lines spanning January 3, 2014 through December 30, 2017. One order can contain multiple lines. Currency values are interpreted as USD. The source uses `DD/MM/YY` dates; postal codes are identifiers, not quantities.

The CSV is included for reproducibility. If missing, run `python src/download_data.py` from the repository root. The downloader uses the pinned revision and does not overwrite an existing CSV.

## Processing

[src/analyze.py](../src/analyze.py) validates the schema, dates, numeric ranges, missing cells, and duplicate identifiers. It retains negative profits, records quality issues, and creates `Year`, `YearMonth`, `Discount Group`, and `Loss Line`.

- [processed/superstore_clean.csv](processed/superstore_clean.csv): typed and enriched dataset for analysis and Power BI, with ISO dates.
- [Data dictionary](../docs/data_dictionary.md): source fields and engineered fields.
- [Quality report](../reports/data_quality/data_quality.json): validation counts and analysis date range.
- [Rejected records](../reports/data_quality/data_quality_issues.csv): records excluded by the implemented checks; header only for the supplied source because none were rejected.

Duplicates are reported rather than silently removed. All 9,994 rows pass the implemented checks for the supplied source. Passing these checks is not a claim that every possible data-quality rule has been tested.

## Attribution and limitations

The source dataset and mirror belong to their respective creators. The supplied project does not contain a verified dataset license. Attribution is preserved; no new license is asserted over the source or derived dataset. Consult the upstream source terms before redistributing or using it beyond this educational project.

The data describes a retail sample and does not support claims about current market conditions, causal discount effects, or realized business improvements. It contains reported profit but no detailed cost ledger.
