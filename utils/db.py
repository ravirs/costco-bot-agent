import os
from supabase import create_client, Client

url: str = os.getenv("SUPABASE_URL", "")
key: str = os.getenv("SUPABASE_KEY", "")

# Initialize client if url and key are provided
if url and key:
    supabase: Client = create_client(url, key)
else:
    # Fallback to None if not configured, useful for local testing without DB initially
    supabase = None
