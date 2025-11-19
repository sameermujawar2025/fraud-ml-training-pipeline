import os
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseModel):
    mongo_uri: str = os.getenv("MONGO_URI","mongodb://localhost:27017")
    mongo_db_name: str = os.getenv("MONGO_DB_NAME","tao-fda-db")
    csv_transactions_path: str = os.getenv("CSV_TRANSACTIONS_PATH","./data/fraud_transactions_full_5000rows_90days.csv")
    csv_blacklist_path: str | None = os.getenv("CSV_BLACKLIST_PATH", None)
    last_hour_ttl_seconds: int = int(os.getenv("LAST_HOUR_TTL_SECONDS","3600"))
    behavior_window_days: int = int(os.getenv("BEHAVIOR_WINDOW_DAYS","60"))
    scheduler_interval_minutes: int = int(os.getenv("SCHEDULER_INTERVAL_MINUTES","10"))

settings = Settings()
