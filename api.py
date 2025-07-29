# Alternative entry point for deployment platforms
# Some platforms look for api.py or app.py
from backend.main import app

# This allows deployment platforms to find the app at:
# - app (from main.py import)
# - api.app (this file)
# - api:app (common pattern)

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)