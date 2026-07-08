# run_api.py
import uvicorn

print("Starting Forex Market Regime Detection API")
print("Press Ctrl+C to stop the server")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)