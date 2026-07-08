# Forex Market Regime Detection

An end-to-end system that identifies distinct **market regimes** (e.g. trending, ranging, high/low volatility) in forex price data using unsupervised machine learning, validates those regimes against real forward returns, and serves the results through an API + live dashboard.

---

## 1. What the system does

Financial markets don't behave the same way all the time — a strategy that works in a trending market can lose money in a choppy one. This system automatically detects which "regime" a currency pair is currently in, so that strategies, risk limits, or trading decisions can be adapted accordingly.

At a high level, the pipeline is:

```
MetaTrader 5  →  Data Validation  →  Feature Engineering  →  Clustering  →  Validation  →  API / Dashboard
 (raw prices)      (data quality)    (technical + wavelet     (regime         (statistical &      (serve live
                                       + PCA features)         labels)         trading checks)      regime data)
```

## 2. Architecture

| Stage | Module | Responsibility |
|---|---|---|
| **Data Acquisition** | `src/data/data_acquisition.py` | Pulls historical OHLC data for multiple pairs and timeframes directly from MetaTrader 5 |
| **Data Validation** | `src/data/data_validation.py` | Checks for gaps, outliers, and data quality issues; produces diagnostic plots |
| **Data Storage** | `src/data/data_storage.py`, `migrate_data.py` | Persists raw/processed data and manages storage migrations |
| **Feature Engineering** | `src/features/feature_engineering.py` | Builds technical indicators (volatility, momentum, trend strength, etc.) and scales them |
| **Advanced Features** | `src/features/advanced_feature_engineering.py` | Wavelet decomposition, PCA dimensionality reduction, and cross-timeframe feature integration |
| **Regime Detection** | `src/models/market_regime_detection.py` | Core clustering engine — trains and compares multiple algorithms |
| **Model Training** | `src/models/train_and_save_models.py`, `train.py` | Trains final models per symbol/timeframe and persists them (`.joblib`) |
| **Validation** | `src/validation/regime_validation.py` | Statistical validation (silhouette, Davies-Bouldin, Calinski-Harabasz), regime stability/persistence, and forward-return / trading-performance backtests |
| **API** | `api/api.py` | FastAPI service exposing prices, regimes, model info, and strategy performance |
| **Dashboard** | `src/visualization/dashboard.py`, `api/static/dashboard.html` | Live/interactive view of current regimes (Dash/Plotly + a static web dashboard) |

**Currency pairs covered:** EUR/USD, GBP/USD, USD/JPY
**Timeframes covered:** H1, H4, D1

## 3. Machine learning approach

The system trains and compares **four clustering strategies** per symbol/timeframe and keeps whichever performs best:

- **K-Means** — fast, well-defined regime centroids
- **DBSCAN** — density-based, naturally handles noise/outlier periods
- **Gaussian Mixture Models (GMM)** — probabilistic, soft regime boundaries
- **Ensemble** — combines the above for more robust labeling

Feature inputs include technical indicators, **wavelet-transformed** signals (to capture multi-scale trend/cycle behavior), and **PCA-reduced** feature sets (to cut noise and correlated dimensions) before clustering.

## 4. Validation methodology

Rather than trusting cluster labels blindly, every model is validated on:
- **Cluster quality metrics** — silhouette score, Davies-Bouldin index, Calinski-Harabasz index
- **Regime stability** — number of transitions, average regime duration, day-N persistence
- **Forward returns** — statistical significance (p-values) of 1/5/10/20-day forward returns per regime
- **Simulated trading performance** — total/annualized return, Sharpe ratio, max drawdown, win rate for a simple regime-based strategy

Example result (EUR/USD, H1, DBSCAN): 100% regime stability, and a regime-based strategy producing a 4.58% total return with a 0.03 Sharpe ratio over the backtest window — illustrating that some detected regimes carry real, if modest, predictive signal, while validation exists precisely to separate the regimes that do from the ones that don't.

## 5. Serving layer

- **REST API** (`api/api.py`, FastAPI): `/api/prices`, `/api/regimes`, `/api/regime-metrics`, `/api/model-info`, `/api/model-performance`, `/api/strategy`, `/health`
- **Dashboard**: a Dash/Plotly app for live monitoring, plus a static HTML dashboard served directly from the API

## 6. Tech stack

Python · scikit-learn · SciPy · PyWavelets · pandas/NumPy · FastAPI · Dash/Plotly · MetaTrader5 API · joblib

## 7. Project structure

```
forex_regime_detection/
├── api/                  # FastAPI service + static dashboard
├── config/               # Central configuration (pairs, timeframes, paths)
├── src/
│   ├── data/              # Acquisition, validation, storage
│   ├── features/          # Feature engineering (basic + advanced)
│   ├── models/             # Clustering + training
│   ├── validation/          # Statistical & trading validation
│   └── visualization/       # Dashboard
├── data/
│   ├── raw/                # Raw MT5 price history
│   ├── features/            # Engineered feature sets
│   ├── results/              # Trained models (.joblib)
│   └── validation/            # Per-run validation reports & plots
└── tests/                # Unit tests
```

## 8. Getting started

```bash
git clone <your-repo-url>
cd forex_regime_detection
pip install -r requirements.txt

# 1. Pull data (requires a MetaTrader 5 terminal + account)
python src/data/data_acquisition.py

# 2. Engineer features
python src/features/feature_engineering.py

# 3. Train & save regime models
python src/models/train_and_save_models.py

# 4. Validate results
python src/validation/regime_validation.py

# 5. Serve the API + dashboard
python api/run_api.py
```

## 9. Demo

`demo/forex_regime_dashboard.html` is a standalone, static presentation demo — no server or MetaTrader 5 connection required. It embeds real regime labels and validation metrics (silhouette, Davies-Bouldin, backtest return/Sharpe/drawdown/win rate) pulled directly from `data/results/` and `data/validation/`, for EUR/USD, GBP/USD, and USD/JPY across H1/H4/D1. Just open it in a browser. It's a snapshot for talks and reviews; the live system serves the same underlying data through the FastAPI service and Dash dashboard described above.

## 10. Presentation talking points

- **Problem**: static trading strategies underperform because markets shift between trending, ranging, and volatile states.
- **Approach**: unsupervised clustering on engineered technical/wavelet/PCA features to auto-label market regimes, per currency pair and timeframe.
- **Rigor**: multiple algorithms are compared and validated not just on cluster quality but on out-of-sample forward returns and simulated trading performance — so "good clusters" and "profitable regimes" aren't conflated.
- **Productionization**: results are exposed via a FastAPI service and a live dashboard, so regime state can plug into downstream trading or risk systems in real time.

---

*This README was generated to support a project walkthrough/presentation.*
