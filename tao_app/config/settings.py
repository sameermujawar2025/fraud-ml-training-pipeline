import os
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseModel):
    mongo_uri: str = os.getenv("MONGO_URI","mongodb://localhost:27017")
    mongo_db_name: str = os.getenv("MONGO_DB_NAME","tao-fda-db")
    csv_transactions_path: str = os.getenv("CSV_TRANSACTIONS_PATH","./data/transaction_90_days_5000_rows.csv")
    csv_blacklist_path: str | None = os.getenv("CSV_BLACKLIST_PATH", "./data/blacklist.csv")
    behavior_window_days: int = int(os.getenv("BEHAVIOR_WINDOW_DAYS","90"))
    # NEW FIELD → FIX FOR YOUR ERROR
    last_90d_ttl_seconds: int = int(os.getenv("LAST_90D_TTL_SECONDS", str(90 * 24 * 3600)))
    scheduler_interval_minutes: int = int(os.getenv("SCHEDULER_INTERVAL_MINUTES","10"))

settings = Settings()
