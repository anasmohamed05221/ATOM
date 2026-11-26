# ATOM Project Journal

A recap of each phase, written when the phase is finished: what we did, what we saw, what we learned and what we decided.
Each decision's reason lives in the [Decision Log](DECISIONS.md).

---

## Phase 1 · Choosing the dataset (Issue #1) · 25–26 Nov 2026

### Goal
Find a public, well-documented flight-price dataset that fits ATOM: predict ticket prices (regression), and possibly a "buy now or wait" extension.

### What we did
1. **Read the course materials** to stay in scope. Key requirements: the dataset must be public and well documented; cross-validation is expected; the defense focuses most on the data (why this dataset, how it was cleaned, why each algorithm).
2. **Compared three candidate datasets** and checked each license at the source:

   | Option | Dataset | Size | License | Outcome |
   |---|---|---|---|---|
   | A | EaseMyTrip flights (India, Feb–Mar 2022) | 55 MB, ~300k rows | CC0 | Rejected: we preferred US data with repeated price checks per flight |
   | B | [Expedia flights (USA, Apr–Oct 2022)](https://www.kaggle.com/datasets/dilwong/flightprices) by Dillon Wong | 31 GB, 82M rows | CC BY 4.0 | **Chosen** |
   | C | US DOT Consumer Airfare Report, Table 1a (1993–2026) | ~10 MB, ~262k rows | Public domain | Rejected: each row is a route's quarterly *average* fare, not a ticket, so buy-or-wait is impossible |

3. **Downloaded option B** from Kaggle (5.9 GB zipped, one file: `itineraries.csv`, 31 GB unzipped). We read it straight from the zip, so it never needed unzipping.
4. **Cut it down to 3% of flights** with [scripts/make_sample.py](../scripts/make_sample.py).
5. **Set up the project**: Python with `uv`, plus pandas, scikit-learn, matplotlib and Jupyter. Data files and Kaggle keys are excluded from git.
6. **First look at the data** in [notebooks/01_explore.ipynb](../notebooks/01_explore.ipynb): size, first rows, missing values, price summary, one flight's price over time.

### What we learned
- **How the data was collected:** a program checked Expedia every day and recorded ticket prices, not real people's searches. So **the same flight appears many times**, once per day it was checked. That's what makes buy-or-wait possible.
- **The data is too big for memory:** 31 GB against 16 GB of RAM. Reading it piece by piece works, but training a model needs all rows in memory at once, so we had to cut it.
- **Sampling random rows would break each flight's price history.** So we sampled whole flights: we turned each flight's ID (`legId`) into a fixed number from 0 to 99 and kept flights below 3. That's reproducible: the same flights are chosen every time.
- **Leakage traps we spotted early:**
  - `baseFare` is almost the same as the target `totalFare`, so it must be removed.
  - `legId` is an ID, not a feature (the model would memorize it), but we keep it to split by flight.
  - The same flight on nearby days in both training and test would let the model peek, so the split must be **by flight, not by row**.

### Result
| | Full dataset | Our sample |
|---|---|---|
| Rows | 82,138,753 | **2,461,647** (3.00%) |
| Unique flights | — | **179,952** |
| Size | 31 GB | **214 MB** (`data/processed/flights_sample_3pct.parquet`) |

### Decisions made
[#1 Regression first](DECISIONS.md) · [#2 Expedia dataset](DECISIONS.md) · [#3 Sample whole flights](DECISIONS.md)

### Challenges
- Dataset size was larger than the computer's memory, which we solved by sampling whole flights.
- Licenses weren't visible in web searches, so we confirmed them through Kaggle's own dataset information.
