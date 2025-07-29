"""
Startup script to ensure production readiness
"""
import os
import json
from datetime import datetime
from cache_manager import cache_manager

def check_cache_status():
    """Check if we have any cached data available"""
    cache_dir = "../data/cache"
    
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        return False
    
    # Check for any cached files
    cache_files = [f for f in os.listdir(cache_dir) if f.endswith('.json')]
    
    if len(cache_files) == 0:
        print("WARNING: No cached data found. API will rely on real-time data fetching.")
        print("Consider running prefetch_data.py to populate cache.")
        return False
    
    print(f"Found {len(cache_files)} cached data files")
    
    # Check prefetch status
    status_file = os.path.join(cache_dir, "prefetch_status.json")
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            status = json.load(f)
        print(f"Last prefetch run: {status.get('last_run', 'Unknown')}")
        print(f"Stocks cached: {status.get('success_count', 0)}")
    
    return True

def ensure_directories():
    """Ensure all required directories exist"""
    dirs = [
        "../data/cache",
        "../data/summaries", 
        "../data/transcripts",
        "../data/historical",
        "../data/analyses",
        "../data/transcripts/full"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    print("All required directories verified")

def startup():
    """Run startup checks"""
    print("=== Investor Edge Backend Startup ===")
    print(f"Time: {datetime.now()}")
    
    # Ensure directories exist
    ensure_directories()
    
    # Check cache status
    has_cache = check_cache_status()
    
    if not has_cache:
        print("\n⚠️  No cache found. Initializing with default data...")
        from init_cache import init_cache
        init_cache()
        has_cache = check_cache_status()
    
    if has_cache:
        print("\n✅ Cache data available. Application ready.")
    else:
        print("\n⚠️  WARNING: Running without cached data.")
        print("The application will fetch real-time data which may be rate-limited.")
    
    print("=====================================\n")

if __name__ == "__main__":
    startup()