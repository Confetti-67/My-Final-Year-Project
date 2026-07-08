"""
Configuration parameters for the forex regime detection system.
"""

import os
from datetime import datetime, timedelta
from pathlib import Path

# Project structure - Using Path for better Windows compatibility
PROJECT_ROOT = Path(__file__).parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
VISUALIZATION_DIR = DATA_DIR / "visualizations"
MODEL_DIR = PROJECT_ROOT / "models"

# Ensure directories exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, VISUALIZATION_DIR, MODEL_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# Data acquisition parameters
CURRENCY_PAIRS = ["EURUSD", "GBPUSD", "USDJPY"]
TIMEFRAMES = {
    "1H": "H1",  # 1 hour
    "4H": "H4",  # 4 hour
    "1D": "D1",  # Daily
}

# Default date ranges (can be overridden)
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=5*365)  # 5 years of data

# MetaTrader5 parameters
# MT5_TERMINAL_PATH is optional - if not specified, the script will try to connect without a path
# MT5_TERMINAL_PATH = r"C:\Users\peter\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"  
MT5_LOGIN = None  # For demo account, you can leave this as None
MT5_PASSWORD = None  # For demo account, you can leave this as None
MT5_SERVER = None  # For demo account, you can leave this as None

# Feature engineering parameters
PCA_VARIANCE_THRESHOLD = 0.95  # Keep features that explain 95% of variance
WAVELET_DECOMPOSITION_LEVEL = 3
FEATURE_WINDOW_SIZES = [14, 30, 60, 90]  # Different lookback periods

# Clustering parameters
KMEANS_MAX_CLUSTERS = 10
DBSCAN_EPS_RANGE = [0.1, 0.5]
DBSCAN_MIN_SAMPLES_RANGE = [5, 20]
GMM_MAX_COMPONENTS = 10

# Validation parameters
CONFIDENCE_LEVEL = 0.95
SILHOUETTE_SCORE_THRESHOLD = 0.6
DAVIES_BOULDIN_THRESHOLD = 0.5
CALINSKI_HARABASZ_THRESHOLD = 100

# System performance parameters
MAX_LATENCY_MS = 100
PROCESSING_EVENTS_PER_SECOND = 10000

# Add database configuration to config.py
DB_CONFIG = {
    'DB_USER': 'postgres',
    'DB_PASSWORD': 'Peter@martin0157',  # Change this!
    'DB_HOST': 'localhost',
    'DB_PORT': '5432',
    'DB_NAME': 'forex_regime_detection'
}