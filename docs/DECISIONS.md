# ATOM Decision Log

Every key decision, with the reason in one sentence. Use this to prepare for the defense.

| # | Decision | Why |
|---|---|---|
| 1 | Regression first (predict the price); buy-or-wait classification only as an optional extension | Regression is the core goal; buy-or-wait needs each flight's price recorded on many days, so we add it only if time and data allow. |
| 2 | Dataset: [Flight Prices (Expedia, USA, 2022)](https://www.kaggle.com/datasets/dilwong/flightprices) by Dillon Wong, CC BY 4.0 | It records the same flight's price on different search dates, which supports our optional buy-or-wait extension and shows how a single flight's price changes; it is publicly available (CC BY 4.0) with every column documented. |
| 3 | Cut the 31 GB dataset by sampling about 3% of whole flights (all rows of each chosen flight) | To make sure we don't lose the price history of our chosen flights, because the buy-or-wait extension needs each flight's full history. |

## Notes for later steps
- **Split by flight, not by row** (issue #2): all rows of one flight go to training or to testing, never both. Otherwise the model sees the same flight's price on nearby days, which is leakage.
- **`baseFare` is leakage** when predicting `totalFare`: it is almost the same number. Remove it.
