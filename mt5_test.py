"""
Simplified test for MetaTrader5 connection without specific path.

This script attempts to connect to MT5 without specifying the terminal path.
"""

import sys
from datetime import datetime, timedelta

try:
    import MetaTrader5 as mt5
    print("MetaTrader5 package imported successfully")
except ImportError:
    print("ERROR: MetaTrader5 package not found")
    print("Please install it using: pip install MetaTrader5")
    sys.exit(1)

print("Attempting to connect to MetaTrader5 without specifying path...")

# Initialize MT5 without path
if not mt5.initialize():
    error = mt5.last_error()
    print(f"ERROR: Failed to initialize MT5: {error}")
    
    if error[0] == 10:
        print("This could be because MetaTrader5 is not running.")
        print("Please launch MetaTrader5 and try again.")
    sys.exit(1)

# Check if connection was successful
print(f"Successfully connected to MetaTrader5!")
print(f"Terminal info: {mt5.terminal_info()}")
print(f"MetaTrader5 version: {mt5.version()}")

# Test with fetching some simple data
print("\nAttempting to fetch some basic symbol data...")
symbols = ["EURUSD", "GBPUSD", "USDJPY"]

for symbol in symbols:
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is not None:
        print(f"Found symbol: {symbol}")
    else:
        print(f"Symbol not found: {symbol}")

# Try to get some recent OHLC data
print("\nAttempting to fetch recent EUR/USD data...")
end_date = datetime.now()
start_date = end_date - timedelta(days=1)

try:
    rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_H1, start_date, end_date)
    if rates is not None and len(rates) > 0:
        print(f"Successfully fetched {len(rates)} bars of EUR/USD H1 data")
    else:
        print("Failed to fetch EUR/USD data")
except Exception as e:
    print(f"Error fetching data: {str(e)}")

# Shutdown
mt5.shutdown()
print("\nTest completed and connection closed")